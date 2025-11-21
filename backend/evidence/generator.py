import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import json


class EvidenceGenerator:
    """Generate evidence kits and takedown requests"""
    
    def __init__(self, output_dir="./evidence_kits"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_evidence_kit(self, brand, suspicious_app, detection):
        """Create a comprehensive evidence kit PDF"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{brand.name}_{suspicious_app.package_id}_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("FAKE APP DETECTION EVIDENCE KIT", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Summary Box
        story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
        
        summary_data = [
            ["Detection ID:", str(detection.id)],
            ["Risk Level:", detection.risk_level],
            ["Confidence Score:", f"{detection.confidence_score:.2%}"],
            ["Date Detected:", detection.detected_at.strftime("%Y-%m-%d %H:%M:%S")],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Legitimate App Information
        story.append(Paragraph("LEGITIMATE APPLICATION", heading_style))
        
        legit_data = [
            ["Brand Name:", brand.name],
            ["Developer:", brand.developer_name],
            ["Official Package IDs:", ", ".join(brand.package_ids[:3])],
        ]
        
        legit_table = Table(legit_data, colWidths=[2*inch, 4*inch])
        legit_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#d5f4e6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(legit_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Suspicious App Information
        story.append(Paragraph("SUSPICIOUS APPLICATION", heading_style))
        
        susp_data = [
            ["App Name:", suspicious_app.app_name],
            ["Package ID:", suspicious_app.package_id],
            ["Developer:", suspicious_app.developer_name],
            ["Source:", suspicious_app.source],
            ["Downloads:", str(suspicious_app.download_count)],
            ["Rating:", f"{suspicious_app.rating:.1f}" if suspicious_app.rating else "N/A"],
            ["Store URL:", suspicious_app.store_url],
        ]
        
        susp_table = Table(susp_data, colWidths=[2*inch, 4*inch])
        susp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fadbd8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(susp_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Detection Analysis
        story.append(Paragraph("DETECTION ANALYSIS", heading_style))
        
        analysis_data = [
            ["Icon Similarity:", f"{detection.icon_similarity_score:.2%}"],
            ["Name Similarity:", f"{detection.text_similarity_score:.2%}"],
            ["Certificate Match:", "NO" if not detection.certificate_match else "YES"],
            ["Review Fraud Score:", f"{detection.review_fraud_score:.2%}"],
            ["Overall Confidence:", f"{detection.confidence_score:.2%}"],
        ]
        
        analysis_table = Table(analysis_data, colWidths=[2*inch, 4*inch])
        analysis_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fff4e6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(analysis_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Detection Reasons
        story.append(Paragraph("EVIDENCE & REASONING", heading_style))
        
        reasons_text = "<br/>".join([f"• {reason}" for reason in detection.detection_reasons])
        story.append(Paragraph(reasons_text, styles['BodyText']))
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendation
        story.append(Paragraph("RECOMMENDATION", heading_style))
        
        if detection.risk_level in ["CRITICAL", "HIGH"]:
            recommendation = """
            Based on the high confidence score and multiple similarity indicators, 
            we strongly recommend immediate takedown of this application. The app 
            exhibits clear signs of impersonation and poses a significant risk to 
            users who may mistake it for the legitimate application.
            """
        else:
            recommendation = """
            The application shows moderate similarity to the legitimate app. 
            We recommend further investigation and monitoring. If additional 
            evidence is gathered, a takedown request should be filed.
            """
        
        story.append(Paragraph(recommendation, styles['BodyText']))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def create_takedown_request(self, brand, suspicious_app, detection, store):
        """Generate takedown request text for app stores"""
        
        if store == "play_store":
            return self._generate_play_store_request(brand, suspicious_app, detection)
        elif store == "app_store":
            return self._generate_app_store_request(brand, suspicious_app, detection)
        else:
            return self._generate_generic_request(brand, suspicious_app, detection)
    
    def _generate_play_store_request(self, brand, suspicious_app, detection):
        """Generate Google Play Store takedown request"""
        
        request = f"""
Subject: Trademark Infringement / Impersonation - {suspicious_app.app_name}

Dear Google Play Store Team,

I am writing to report a mobile application that infringes on our trademark and impersonates our official application.

LEGITIMATE APPLICATION:
- Brand Name: {brand.name}
- Developer: {brand.developer_name}
- Official Package IDs: {', '.join(brand.package_ids)}

INFRINGING APPLICATION:
- App Name: {suspicious_app.app_name}
- Package ID: {suspicious_app.package_id}
- Developer: {suspicious_app.developer_name}
- Store URL: {suspicious_app.store_url}

EVIDENCE OF INFRINGEMENT:
1. Icon Similarity: {detection.icon_similarity_score:.2%} match with our official app
2. Name Similarity: {detection.text_similarity_score:.2%} match with our brand name
3. Certificate Mismatch: The app is not signed with our official certificate
4. Overall Confidence: {detection.confidence_score:.2%}

SPECIFIC VIOLATIONS:
{self._format_reasons(detection.detection_reasons)}

This application misleads users into believing it is affiliated with our brand, 
which violates Google Play's policy on impersonation and intellectual property rights.

We request immediate removal of this application from the Google Play Store.

Attached: Detailed evidence kit with visual comparisons and analysis.

Thank you for your prompt attention to this matter.

Best regards,
Brand Protection Team
{brand.name}
"""
        return request
    
    def _generate_app_store_request(self, brand, suspicious_app, detection):
        """Generate Apple App Store takedown request"""
        
        request = f"""
Subject: Trademark Violation Report - {suspicious_app.app_name}

To Apple App Store Review Team,

We are reporting an application that infringes on our intellectual property rights 
and impersonates our official mobile application.

LEGITIMATE APP INFORMATION:
Brand: {brand.name}
Developer: {brand.developer_name}
Official Bundle IDs: {', '.join(brand.package_ids)}

INFRINGING APP INFORMATION:
Name: {suspicious_app.app_name}
Bundle ID: {suspicious_app.package_id}
Developer: {suspicious_app.developer_name}

INFRINGEMENT EVIDENCE:
- Visual similarity score: {detection.icon_similarity_score:.2%}
- Brand name similarity: {detection.text_similarity_score:.2%}
- Detection confidence: {detection.confidence_score:.2%}

{self._format_reasons(detection.detection_reasons)}

This app violates App Store Review Guidelines regarding intellectual property 
and may cause user confusion.

We request immediate removal of this application.

Evidence documentation attached.

Respectfully,
Legal Department
{brand.name}
"""
        return request
    
    def _generate_generic_request(self, brand, suspicious_app, detection):
        """Generate generic takedown request"""
        
        return f"""
Takedown Request: {suspicious_app.app_name}

Brand: {brand.name}
Suspicious App: {suspicious_app.app_name} ({suspicious_app.package_id})
Confidence Score: {detection.confidence_score:.2%}
Risk Level: {detection.risk_level}

Evidence: See attached evidence kit for detailed analysis.
"""
    
    def _format_reasons(self, reasons):
        """Format detection reasons as bullet points"""
        return '\n'.join([f"• {reason}" for reason in reasons])


# Usage example
if __name__ == "__main__":
    # Mock data for demonstration
    class MockBrand:
        name = "PayPal"
        developer_name = "PayPal, Inc."
        package_ids = ["com.paypal.android.p2pmobile"]
    
    class MockApp:
        app_name = "PayPal Pro"
        package_id = "com.paypal.android.fake"
        developer_name = "Unknown Developer"
        source = "play_store"
        download_count = 10000
        rating = 4.5
        store_url = "https://play.google.com/store/apps/..."
    
    class MockDetection:
        id = 12345
        icon_similarity_score = 0.92
        text_similarity_score = 0.89
        certificate_match = False
        review_fraud_score = 0.75
        confidence_score = 0.94
        risk_level = "CRITICAL"
        detection_reasons = [
            "Icon similarity: 92%",
            "Name similarity: 89%",
            "Certificate mismatch detected",
            "Review fraud patterns detected"
        ]
        detected_at = datetime.now()
    
    generator = EvidenceGenerator()
    
    # Generate evidence kit
    pdf_path = generator.create_evidence_kit(MockBrand(), MockApp(), MockDetection())
    print(f"Evidence kit generated: {pdf_path}")
    
    # Generate takedown request
    request = generator.create_takedown_request(MockBrand(), MockApp(), MockDetection(), "play_store")
    print(f"\\nTakedown Request:\\n{request}")
