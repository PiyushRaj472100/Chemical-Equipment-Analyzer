from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from django.db.models import Q
import pandas as pd
import io
from .models import Dataset
from .serializers import DatasetSerializer, SummarySerializer, UserSerializer
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime


class RegisterView(APIView):
    """
    API endpoint for user registration.
    POST /api/register/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password')
        email = (request.data.get('email') or '').strip()
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email__iexact=email).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not username:
            username = email.split('@')[0]
            base = username
            suffix = 1
            while User.objects.filter(username=username).exists():
                suffix += 1
                username = f"{base}{suffix}"
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        return Response(
            {'message': 'User registered successfully', 'username': username, 'email': email},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    API endpoint for user login.
    POST /api/login/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = (request.data.get('email') or '').strip()
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        matched = User.objects.filter(email__iexact=email)
        if not matched.exists():
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if matched.count() > 1:
            return Response(
                {'error': 'Multiple accounts found for this email. Contact admin.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_obj = matched.first()
        user = authenticate(username=user_obj.username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_200_OK)


class UploadCSVView(APIView):
    """
    API endpoint to upload and process CSV files.
    POST /api/upload/
    """
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        csv_file = request.FILES['file']
        
        # Validate file extension
        if not csv_file.name.endswith('.csv'):
            return Response(
                {'error': 'File must be a CSV'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read CSV file using pandas
            csv_data = csv_file.read().decode('utf-8')
            df = pd.read_csv(io.StringIO(csv_data))
            
            # Validate required columns
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {'error': f'Missing required columns: {", ".join(missing_columns)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Perform data analytics using Pandas
            total_equipment = len(df)
            
            # Compute averages
            average_flowrate = float(df['Flowrate'].mean())
            average_pressure = float(df['Pressure'].mean())
            average_temperature = float(df['Temperature'].mean())
            
            # Compute equipment type distribution
            type_distribution = df['Type'].value_counts().to_dict()
            
            # Store dataset in database with user association
            dataset = Dataset.objects.create(
                user=request.user,
                name=csv_file.name,
                total_equipment=total_equipment,
                average_flowrate=average_flowrate,
                average_pressure=average_pressure,
                average_temperature=average_temperature,
                type_distribution=type_distribution
            )
            
            # Maintain only last 5 datasets per user
            Dataset.maintain_limit_per_user(request.user, 5)
            
            # Prepare response
            response_data = {
                'message': 'CSV file uploaded and processed successfully',
                'dataset_id': dataset.id,
                'summary': {
                    'total_equipment': total_equipment,
                    'average_values': {
                        'flowrate': round(average_flowrate, 2),
                        'pressure': round(average_pressure, 2),
                        'temperature': round(average_temperature, 2)
                    },
                    'type_distribution': type_distribution
                },
                'equipment_data': df.to_dict('records')
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except pd.errors.EmptyDataError:
            return Response(
                {'error': 'CSV file is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Error processing CSV: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SummaryView(APIView):
    """
    API endpoint to get summary of the most recent uploaded dataset.
    GET /api/summary/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Get the most recent dataset for the authenticated user
        latest_dataset = Dataset.objects.filter(user=request.user).first()
        
        if not latest_dataset:
            return Response(
                {'error': 'No datasets available'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prepare summary response
        summary_data = {
            'total_equipment': latest_dataset.total_equipment,
            'average_values': {
                'flowrate': round(latest_dataset.average_flowrate, 2),
                'pressure': round(latest_dataset.average_pressure, 2),
                'temperature': round(latest_dataset.average_temperature, 2)
            },
            'type_distribution': latest_dataset.type_distribution,
            'upload_date': latest_dataset.upload_timestamp,
            'dataset_name': latest_dataset.name
        }
        
        return Response(summary_data, status=status.HTTP_200_OK)


class HistoryView(APIView):
    """
    API endpoint to get history of uploaded datasets.
    GET /api/history/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Get last 5 datasets for the authenticated user
        datasets = Dataset.objects.filter(user=request.user)[:5]
        
        if not datasets:
            return Response(
                {'message': 'No dataset history available', 'datasets': []},
                status=status.HTTP_200_OK
            )
        
        serializer = DatasetSerializer(datasets, many=True)
        
        return Response({
            'count': len(serializer.data),
            'datasets': serializer.data
        }, status=status.HTTP_200_OK)


class GeneratePDFReportView(APIView):
    """
    API endpoint to generate PDF report for a dataset.
    GET /api/generate-pdf/<dataset_id>/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, dataset_id=None):
        try:
            if dataset_id:
                # Get specific dataset
                dataset = Dataset.objects.filter(id=dataset_id, user=request.user).first()
            else:
                # Get latest dataset
                dataset = Dataset.objects.filter(user=request.user).first()
            
            if not dataset:
                return Response(
                    {'error': 'Dataset not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create HTTP response with PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
            
            # Create PDF
            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#667eea'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#764ba2'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            # Title
            title = Paragraph("Chemical Equipment Analysis Report", title_style)
            elements.append(title)
            elements.append(Spacer(1, 0.2*inch))
            
            # Report Info
            info_data = [
                ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Dataset Name:', dataset.name],
                ['Upload Date:', dataset.upload_timestamp.strftime('%Y-%m-%d %H:%M:%S')],
                ['User:', request.user.username],
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Summary Statistics
            summary_heading = Paragraph("Summary Statistics", heading_style)
            elements.append(summary_heading)
            
            summary_data = [
                ['Metric', 'Value'],
                ['Total Equipment', str(dataset.total_equipment)],
                ['Average Flowrate', f"{dataset.average_flowrate:.2f}"],
                ['Average Pressure', f"{dataset.average_pressure:.2f}"],
                ['Average Temperature', f"{dataset.average_temperature:.2f}"],
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # Equipment Type Distribution
            dist_heading = Paragraph("Equipment Type Distribution", heading_style)
            elements.append(dist_heading)
            
            dist_data = [['Equipment Type', 'Count']]
            for eq_type, count in dataset.type_distribution.items():
                dist_data.append([eq_type, str(count)])
            
            dist_table = Table(dist_data, colWidths=[3*inch, 3*inch])
            dist_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
            ]))
            elements.append(dist_table)
            
            # Build PDF
            doc.build(elements)
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )