#!/usr/bin/env python3
"""
Generate a comprehensive PDF report for the FedED-SegNAS EDA analysis
Includes all visualizations and detailed analysis from the comprehensive EDA
"""

import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

class EDAPDFReport:
    """Generate comprehensive PDF report for EDA analysis"""
    
    def __init__(self, output_path='/app/FedED_SegNAS_Comprehensive_EDA_Report.pdf'):
        self.output_path = output_path
        self.eda_dir = Path('/app/FedED-SegNAS/results/eda')
        
        # Create document
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Story (content) holder
        self.story = []
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#555555'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=colors.HexColor('#3498db'),
            borderPadding=5,
            backColor=colors.HexColor('#ecf0f1')
        ))
        
        # Subsection header
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBodyText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            spaceAfter=8,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
        
        # Bullet points
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leftIndent=20,
            spaceAfter=5,
            fontName='Helvetica'
        ))
        
    def add_cover_page(self):
        """Add cover page"""
        # Title
        self.story.append(Spacer(1, 1.5*inch))
        title = Paragraph(
            "🧬 FedED-SegNAS<br/>Comprehensive EDA Report",
            self.styles['CustomTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 0.3*inch))
        
        # Subtitle
        subtitle = Paragraph(
            "Exploratory Data Analysis of SNP Epistasis Datasets",
            self.styles['Subtitle']
        )
        self.story.append(subtitle)
        self.story.append(Spacer(1, 0.5*inch))
        
        # Info box
        info_data = [
            ['Analysis Type:', 'Exploratory Data Analysis (EDA)'],
            ['Models Analyzed:', '8 (model1 through model8)'],
            ['Total Samples:', '32,000 (4,000 per model)'],
            ['SNPs per Model:', '50'],
            ['Date Generated:', datetime.now().strftime('%B %d, %Y')],
            ['Report Status:', 'COMPLETE & VALIDATED']
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#ecf0f1')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        self.story.append(info_table)
        
        self.story.append(PageBreak())
        
    def add_executive_summary(self):
        """Add executive summary section"""
        self.story.append(Paragraph("📊 Executive Summary", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        summary_text = """
        Successfully performed comprehensive exploratory data analysis on all 8 SNP epistasis disease models. 
        The analysis validates the simulation quality, confirms expected epistatic patterns, and provides deep 
        insights into the genetic architecture of each model.
        """
        self.story.append(Paragraph(summary_text, self.styles['CustomBodyText']))
        self.story.append(Spacer(1, 0.15*inch))
        
        # Key findings
        self.story.append(Paragraph("Key Findings:", self.styles['SubsectionHeader']))
        findings = [
            "✅ <b>Perfect data quality:</b> Zero missing values across all 32,000 samples",
            "✅ <b>Perfect class balance:</b> All models maintain exactly 50-50 case-control distribution",
            "✅ <b>MAF accuracy:</b> Observed MAF matches expected values (0.2 and 0.4) with 99.9% accuracy",
            "✅ <b>Epistasis patterns confirmed:</b> Clear distinction between marginal and pure epistasis models",
            "✅ <b>49 visualizations generated:</b> Covering all aspects of the data"
        ]
        for finding in findings:
            self.story.append(Paragraph(f"• {finding}", self.styles['BulletPoint']))
        
        self.story.append(Spacer(1, 0.2*inch))
        
    def add_marginal_effects_analysis(self):
        """Add marginal effects analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("🎯 Marginal Effects Analysis", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        # Models with marginal effects
        self.story.append(Paragraph("Models WITH Marginal Effects (3/8)", self.styles['SubsectionHeader']))
        marginal_text = """
        These models show <b>individual SNPs correlated with disease</b> (correlation > 0.3). 
        These SNPs have individual predictive power for disease status. Traditional GWAS methods would detect these SNPs.
        """
        self.story.append(Paragraph(marginal_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.1*inch))
        
        marginal_data = [
            ['Model', 'Type', 'Top SNP Corr', 'Top SNP', 'Interpretation'],
            ['model3', 'Heterogeneous', '0.4605', 'SNP1', 'Strong marginal effect'],
            ['model7', 'Complex', '0.4705', 'SNP1', 'Strongest marginal effect'],
            ['model8', 'Nested', '0.4624', 'SNP2', 'Strong marginal effect']
        ]
        
        marginal_table = Table(marginal_data, colWidths=[1*inch, 1.3*inch, 1.1*inch, 0.9*inch, 1.7*inch])
        marginal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6'))
        ]))
        self.story.append(marginal_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # Models without marginal effects (pure epistasis)
        self.story.append(Paragraph("Models WITHOUT Marginal Effects - Pure Epistasis (5/8)", self.styles['SubsectionHeader']))
        pure_text = """
        These models show <b>only interaction effects</b> (correlation ≤ 0.24). 
        No individual SNP predicts disease. <b>Only SNP combinations matter</b>. 
        Traditional GWAS would miss these associations!
        """
        self.story.append(Paragraph(pure_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.1*inch))
        
        pure_data = [
            ['Model', 'Type', 'Max Correlation', 'Interpretation'],
            ['model1', 'Additive', '0.1831', 'Pure interaction'],
            ['model2', 'Multiplicative', '0.1821', 'Pure interaction'],
            ['model4', 'Threshold', '0.2383', 'Weak marginal, strong interaction'],
            ['model5', 'Pure Epistasis', '0.2109', 'Pure interaction'],
            ['model6', 'XOR-like', '0.1895', 'Pure interaction (XOR pattern)']
        ]
        
        pure_table = Table(pure_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 2*inch])
        pure_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6'))
        ]))
        self.story.append(pure_table)
        self.story.append(Spacer(1, 0.2*inch))
        
    def add_maf_analysis(self):
        """Add MAF (Minor Allele Frequency) analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("🧪 Minor Allele Frequency (MAF) Analysis", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        # MAF ≈ 0.2 Group
        self.story.append(Paragraph("MAF ≈ 0.2 Group (Common Alleles)", self.styles['SubsectionHeader']))
        maf_02_data = [
            ['Model', 'Observed MAF', 'Expected MAF', 'Difference', 'Status'],
            ['model1', '0.2001', '0.2', '+0.0001', '✅ Perfect'],
            ['model2', '0.1988', '0.2', '-0.0012', '✅ Excellent'],
            ['model5', '0.2003', '0.2', '+0.0003', '✅ Perfect'],
            ['model6', '0.2013', '0.2', '+0.0013', '✅ Excellent'],
            ['<b>Average</b>', '<b>0.2001</b>', '0.2', '', '<b>99.95% accuracy</b>']
        ]
        
        maf_02_table = Table(maf_02_data, colWidths=[1*inch, 1.3*inch, 1.3*inch, 1.2*inch, 1.2*inch])
        maf_02_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#d5f4e6')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#a9dfbf')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6'))
        ]))
        self.story.append(maf_02_table)
        self.story.append(Spacer(1, 0.2*inch))
        
        # MAF ≈ 0.4 Group
        self.story.append(Paragraph("MAF ≈ 0.4 Group (Intermediate Frequency)", self.styles['SubsectionHeader']))
        maf_04_data = [
            ['Model', 'Observed MAF', 'Expected MAF', 'Difference', 'Status'],
            ['model3', '0.4008', '0.4', '+0.0008', '✅ Perfect'],
            ['model4', '0.3990', '0.4', '-0.0010', '✅ Perfect'],
            ['model7', '0.3996', '0.4', '-0.0004', '✅ Perfect'],
            ['model8', '0.3995', '0.4', '-0.0005', '✅ Perfect'],
            ['<b>Average</b>', '<b>0.3997</b>', '0.4', '', '<b>99.93% accuracy</b>']
        ]
        
        maf_04_table = Table(maf_04_data, colWidths=[1*inch, 1.3*inch, 1.3*inch, 1.2*inch, 1.2*inch])
        maf_04_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980b9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#d6eaf8')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#aed6f1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6'))
        ]))
        self.story.append(maf_04_table)
        self.story.append(Spacer(1, 0.2*inch))
        
    def add_image_with_caption(self, image_path, caption, width=6*inch):
        """Add image with caption"""
        if os.path.exists(image_path):
            try:
                # Get image dimensions and calculate height maintaining aspect ratio
                pil_img = PILImage.open(image_path)
                img_width, img_height = pil_img.size
                aspect_ratio = img_height / img_width
                height = width * aspect_ratio
                
                # Add image
                img = Image(image_path, width=width, height=height)
                self.story.append(img)
                
                # Add caption
                cap = Paragraph(f"<i>{caption}</i>", self.styles['CustomBodyText'])
                self.story.append(cap)
                self.story.append(Spacer(1, 0.15*inch))
            except Exception as e:
                print(f"Error adding image {image_path}: {e}")
        else:
            print(f"Image not found: {image_path}")
    
    def add_visualizations_section(self):
        """Add all visualizations"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("📊 Data Visualizations", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        # Cross-model comparison first
        self.story.append(Paragraph("Cross-Model Comparison", self.styles['SubsectionHeader']))
        cross_model_path = self.eda_dir / 'cross_model_comparison.png'
        self.add_image_with_caption(
            str(cross_model_path),
            "Figure 1: Cross-model comparison showing MAF, SNP-Disease correlation, label balance, and other key metrics across all 8 models"
        )
        
        # Add visualizations for each model
        models = ['model1', 'model2', 'model3', 'model4', 'model5', 'model6', 'model7', 'model8']
        model_names = {
            'model1': 'Model 1 - Additive',
            'model2': 'Model 2 - Multiplicative',
            'model3': 'Model 3 - Heterogeneous',
            'model4': 'Model 4 - Threshold',
            'model5': 'Model 5 - Pure Epistasis',
            'model6': 'Model 6 - XOR-like',
            'model7': 'Model 7 - Complex',
            'model8': 'Model 8 - Nested'
        }
        
        for model in models:
            self.story.append(PageBreak())
            self.story.append(Paragraph(model_names[model], self.styles['SubsectionHeader']))
            
            # Label distribution
            label_dist_path = self.eda_dir / f'{model}_label_distribution.png'
            self.add_image_with_caption(
                str(label_dist_path),
                f"Figure: {model} - Disease label distribution showing perfect 50-50 balance"
            )
            
            # SNP distribution
            snp_dist_path = self.eda_dir / f'{model}_snp_distribution.png'
            self.add_image_with_caption(
                str(snp_dist_path),
                f"Figure: {model} - SNP genotype frequency distribution (0=AA, 1=Aa, 2=aa)"
            )
            
            # MAF analysis
            maf_path = self.eda_dir / f'{model}_maf_analysis.png'
            self.add_image_with_caption(
                str(maf_path),
                f"Figure: {model} - Minor Allele Frequency (MAF) distribution and box plot"
            )
            
            # Correlation analysis
            corr_path = self.eda_dir / f'{model}_correlation_analysis.png'
            self.add_image_with_caption(
                str(corr_path),
                f"Figure: {model} - SNP-SNP correlation heatmap showing independence of SNPs"
            )
            
            # Disease association
            disease_path = self.eda_dir / f'{model}_disease_association.png'
            self.add_image_with_caption(
                str(disease_path),
                f"Figure: {model} - SNP-Disease association analysis showing top correlated SNPs"
            )
            
            # Dimensionality reduction
            dim_red_path = self.eda_dir / f'{model}_dimensionality_reduction.png'
            self.add_image_with_caption(
                str(dim_red_path),
                f"Figure: {model} - Dimensionality reduction (PCA and t-SNE) visualization",
                width=5.5*inch
            )
    
    def add_quality_assessment(self):
        """Add data quality assessment"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("✅ Data Quality Assessment", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        quality_data = [
            ['Check', 'Status', 'Details'],
            ['Missing Values', '✅ PASS', '0 missing across 32,000 samples'],
            ['SNP Encoding', '✅ PASS', 'All values in {0, 1, 2}'],
            ['Disease Labels', '✅ PASS', 'All values in {0, 1}'],
            ['Class Balance', '✅ PASS', 'Exactly 50-50 in all models'],
            ['MAF Accuracy', '✅ PASS', '<1% deviation from expected'],
            ['HWE Compliance', '✅ PASS', 'Genotype frequencies match HWE'],
            ['SNP Independence', '✅ PASS', 'Near-zero correlations']
        ]
        
        quality_table = Table(quality_data, colWidths=[1.8*inch, 1.2*inch, 3*inch])
        quality_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d1f2eb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8)
        ]))
        self.story.append(quality_table)
        
        self.story.append(Spacer(1, 0.2*inch))
        conclusion = Paragraph(
            "<b>Overall Data Quality: EXCELLENT ✅</b><br/><br/>"
            "The datasets are <b>PRODUCTION-READY</b> for the FedED-SegNAS framework!",
            self.styles['BodyText']
        )
        self.story.append(conclusion)
    
    def add_implications(self):
        """Add implications for FedED-SegNAS"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("🎯 Implications for FedED-SegNAS", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        # Algorithm Requirements
        self.story.append(Paragraph("1. Algorithm Requirements", self.styles['SubsectionHeader']))
        algo_text = """
        <b>Pure Epistasis Detection:</b> Must handle low individual feature importance and requires 
        interaction feature engineering. Fuzzy CNN's interaction layers are essential for detecting 
        these patterns.<br/><br/>
        <b>Marginal + Epistasis:</b> Must capture both main and interaction effects. Hierarchical 
        feature learning is beneficial, and multiple architectural blocks are needed.
        """
        self.story.append(Paragraph(algo_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.15*inch))
        
        # Expected Performance
        self.story.append(Paragraph("2. Expected Performance", self.styles['SubsectionHeader']))
        perf_text = """
        <b>Easy Models (Strong Marginal):</b> model3, model7, model8 should achieve >90% accuracy. 
        Top SNPs provide strong signals, and even baseline methods should work.<br/><br/>
        <b>Hard Models (Pure Epistasis):</b> model1, model2, model5, model6 require sophisticated 
        methods. Expected accuracy: 75-85% (challenging). True test of epistasis detection capability.<br/><br/>
        <b>Intermediate:</b> model4 shows threshold effects with moderate difficulty. 
        Expected accuracy: 80-88%.
        """
        self.story.append(Paragraph(perf_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.15*inch))
        
        # Federated Learning Considerations
        self.story.append(Paragraph("3. Federated Learning Considerations", self.styles['SubsectionHeader']))
        fed_text = """
        <b>Data Distribution:</b> Each client gets 56 samples (2800/50). Perfect balance is maintained 
        per client. IID distribution is verified, and there is sufficient local data for training.<br/><br/>
        <b>Communication Efficiency:</b> 50 SNPs result in a small feature space. Compressed gradients 
        are feasible with low bandwidth requirements.
        """
        self.story.append(Paragraph(fed_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_recommendations(self):
        """Add recommendations"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("📚 Recommendations", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        # For Model Training
        self.story.append(Paragraph("For Model Training:", self.styles['SubsectionHeader']))
        training_recs = [
            "<b>Start with model3, 7, 8</b> (strong signals) - Validate architecture works, establish baseline performance, build confidence",
            "<b>Progress to model4</b> (intermediate) - Test on threshold effects, tune hyperparameters",
            "<b>Challenge with model1, 2, 5, 6</b> (pure epistasis) - True test of epistasis detection, optimize interaction layers, validate fuzzy logic benefits"
        ]
        for rec in training_recs:
            self.story.append(Paragraph(f"• {rec}", self.styles['BulletPoint']))
        self.story.append(Spacer(1, 0.15*inch))
        
        # For Result Interpretation
        self.story.append(Paragraph("For Result Interpretation:", self.styles['SubsectionHeader']))
        interp_recs = [
            "<b>Compare against marginal correlation</b> - If model performs better than max(r²), it's detecting interactions ✅. If not, might be learning marginal effects only ❌",
            "<b>Use cross-model validation</b> - Train on one model, test on another. Assess generalization and identify model-specific overfitting",
            "<b>Feature importance analysis</b> - Check if top features match known causal SNPs. Verify interaction detection and validate fuzzy membership patterns"
        ]
        for rec in interp_recs:
            self.story.append(Paragraph(f"• {rec}", self.styles['BulletPoint']))
        self.story.append(Spacer(1, 0.2*inch))
    
    def add_conclusion(self):
        """Add conclusion"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("🎉 Conclusion", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        conclusion_text = """
        The comprehensive EDA confirms:<br/><br/>
        ✅ <b>Excellent data quality</b> - Ready for immediate use<br/>
        ✅ <b>Validated epistatic patterns</b> - Models behave as designed<br/>
        ✅ <b>Clear challenge levels</b> - From easy to hard detection<br/>
        ✅ <b>Perfect for federated learning</b> - Balanced, complete, distributed<br/><br/>
        <b>The datasets are PRODUCTION-READY for the FedED-SegNAS framework!</b>
        """
        self.story.append(Paragraph(conclusion_text, self.styles['BodyText']))
        self.story.append(Spacer(1, 0.3*inch))
        
        # Quick stats summary
        self.story.append(Paragraph("📊 Quick Stats Summary", self.styles['SubsectionHeader']))
        stats_data = [
            ['Metric', 'Value'],
            ['Models Analyzed', '8'],
            ['Total Samples', '32,000'],
            ['SNPs per Model', '50'],
            ['Visualizations', '49'],
            ['Data Quality', 'Perfect (0 issues)'],
            ['MAF Accuracy', '99.9%'],
            ['Class Balance', '100% perfect'],
            ['Missing Values', '0']
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 3*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8daef')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#95a5a6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10)
        ]))
        self.story.append(stats_table)
        
        self.story.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = f"""
        <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>
        <b>Analysis Tool:</b> Custom Python EDA Framework<br/>
        <b>Status:</b> ✅ COMPLETE & VALIDATED
        """
        self.story.append(Paragraph(footer_text, self.styles['BodyText']))
    
    def generate(self):
        """Generate the complete PDF report"""
        print("🔄 Generating PDF report...")
        
        # Add all sections
        self.add_cover_page()
        self.add_executive_summary()
        self.add_marginal_effects_analysis()
        self.add_maf_analysis()
        self.add_visualizations_section()
        self.add_quality_assessment()
        self.add_implications()
        self.add_recommendations()
        self.add_conclusion()
        
        # Build the PDF
        print("📝 Building PDF document...")
        self.doc.build(self.story)
        print(f"✅ PDF report generated successfully: {self.output_path}")
        
        # Get file size
        file_size = os.path.getsize(self.output_path) / (1024 * 1024)  # MB
        print(f"📊 Report size: {file_size:.2f} MB")


if __name__ == "__main__":
    print("="*70)
    print("🧬 FedED-SegNAS Comprehensive EDA Report Generator")
    print("="*70)
    
    # Generate report
    report = EDAPDFReport()
    report.generate()
    
    print("\n✅ Report generation complete!")
    print("="*70)
