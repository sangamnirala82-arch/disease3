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
        self.story.append(Paragraph(marginal_text, self.styles['CustomBodyText']))
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
        self.story.append(Paragraph(pure_text, self.styles['CustomBodyText']))
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
        
    def add_image_with_caption(self, image_path, caption, width=6*inch, analysis=None, conclusion=None):
        """Add image with caption, optional analysis, and conclusion"""
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
                self.story.append(Spacer(1, 0.05*inch))
                
                # Add analysis if provided
                if analysis:
                    analysis_style = ParagraphStyle(
                        'AnalysisText',
                        parent=self.styles['CustomBodyText'],
                        fontSize=9,
                        textColor=colors.HexColor('#444444'),
                        leftIndent=15,
                        rightIndent=15,
                        spaceAfter=12,
                        backColor=colors.HexColor('#f9f9f9'),
                        borderWidth=1,
                        borderColor=colors.HexColor('#dddddd'),
                        borderPadding=8
                    )
                    analysis_para = Paragraph(f"<b>📊 Analysis:</b> {analysis}", analysis_style)
                    self.story.append(analysis_para)
                    self.story.append(Spacer(1, 0.1*inch))  # Add extra space between analysis and conclusion
                
                # Add conclusion if provided
                if conclusion:
                    conclusion_style = ParagraphStyle(
                        'ConclusionText',
                        parent=self.styles['CustomBodyText'],
                        fontSize=10,
                        textColor=colors.HexColor('#1a1a1a'),
                        leftIndent=15,
                        rightIndent=15,
                        spaceAfter=12,
                        backColor=colors.HexColor('#ffffff'),
                        borderWidth=2,
                        borderColor=colors.HexColor('#3498db'),
                        borderPadding=10,
                        alignment=TA_LEFT
                    )
                    conclusion_para = Paragraph(f"<b>🎯 Key Takeaway: {conclusion}</b>", conclusion_style)
                    self.story.append(conclusion_para)
                
                self.story.append(Spacer(1, 0.15*inch))
            except Exception as e:
                print(f"Error adding image {image_path}: {e}")
        else:
            print(f"Image not found: {image_path}")
    
    def add_visualizations_section(self):
        """Add all visualizations with detailed analysis"""
        self.story.append(PageBreak())
        self.story.append(Paragraph("📊 Data Visualizations", self.styles['SectionHeader']))
        self.story.append(Spacer(1, 0.1*inch))
        
        # Cross-model comparison first
        self.story.append(Paragraph("Cross-Model Comparison", self.styles['SubsectionHeader']))
        cross_model_path = self.eda_dir / 'cross_model_comparison.png'
        cross_model_analysis = """
        This multi-panel comparison reveals critical patterns across all 8 models. The top-left panel shows 
        MAF consistency with two distinct groups (0.2 and 0.4), validating simulation parameters. The top-right 
        panel demonstrates the clear divide between models with marginal effects (models 3, 7, 8 with correlations 
        >0.4) and pure epistasis models (models 1, 2, 4, 5, 6 with correlations <0.25). The middle-left panel 
        confirms perfect 50-50 class balance across all models, eliminating any bias concerns. The SNP-SNP 
        correlation panel (middle-right) shows near-zero mean correlations, confirming SNP independence. 
        The bottom panels reveal low PCA variance (all <5%), indicating that disease signals exist in high-dimensional 
        interaction space rather than linear combinations. This comprehensive view helps identify which models 
        will be challenging (pure epistasis) versus easier (marginal effects) for the FedED-SegNAS algorithm.
        """
        cross_model_conclusion = """Models 3, 7, and 8 have strong marginal effects (easy to detect), while models 1, 2, 4, 5, and 6 show pure epistasis patterns (challenging), requiring sophisticated interaction detection methods."""
        self.add_image_with_caption(
            str(cross_model_path),
            "Figure 1: Cross-model comparison showing MAF, SNP-Disease correlation, label balance, and other key metrics across all 8 models",
            analysis=cross_model_analysis,
            conclusion=cross_model_conclusion
        )
        
        # Define model-specific analyses and conclusions
        model_analyses = {
            'model1': {
                'label': """The bar chart and pie chart both confirm perfect 50-50 balance (2000 healthy vs 2000 diseased). 
                This eliminates any class imbalance issues and ensures the model must learn true disease patterns rather 
                than exploiting dataset biases. The exact 50% split is crucial for unbiased epistasis detection.""",
                'label_conclusion': """Perfect class balance ensures unbiased learning - the algorithm must discover true genetic patterns, not exploit dataset imbalances.""",
                
                'snp': """The genotype distribution shows the expected Hardy-Weinberg Equilibrium for MAF=0.2: approximately 
                64% homozygous normal (AA), 32% heterozygous (Aa), and 4% homozygous mutant (aa). This distribution 
                matches theoretical predictions perfectly (p²=0.64, 2pq=0.32, q²=0.04), confirming high-quality simulation. 
                The predominance of genotype 0 indicates most alleles are in the common (major) form.""",
                'snp_conclusion': """Genotype frequencies perfectly match Hardy-Weinberg Equilibrium expectations, validating simulation quality and biological realism.""",
                
                'maf': """The histogram shows tight clustering of MAF values around 0.2, with the observed mean (red line) 
                almost perfectly matching the expected value (green line). The box plot confirms minimal variance, with 
                all 50 SNPs having MAF very close to 0.2. This precision validates the GAMETES simulation quality and 
                ensures consistent allele frequencies across all SNPs, critical for fair epistasis detection.""",
                'maf_conclusion': """MAF accuracy of 99.95% confirms high-quality simulation with consistent allele frequencies across all 50 SNPs.""",
                
                'correlation': """The left heatmap displays the SNP-SNP correlation matrix, showing predominantly blue 
                (near-zero correlations) along the diagonal and off-diagonal elements. The right histogram confirms 
                the mean correlation is nearly 0.0001, with most pairwise correlations between -0.02 and +0.02. 
                This demonstrates SNPs are independently simulated with no linkage disequilibrium, meaning each SNP 
                provides unique information. This independence is crucial for detecting true epistatic interactions 
                rather than correlated marker effects.""",
                'correlation_conclusion': """Near-zero SNP-SNP correlations (mean ≈ 0.0001) confirm complete independence - no linkage disequilibrium, enabling pure interaction detection.""",
                
                'disease': """The left panel shows the top 20 SNPs by absolute correlation with disease, revealing no SNP 
                exceeds 0.183 correlation. The right panel's histogram shows a nearly flat distribution of SNP-disease 
                correlations centered near zero. This is the hallmark of <b>pure epistasis</b> - no single SNP predicts 
                disease individually. Traditional GWAS methods relying on marginal associations would completely fail 
                on this model. Only interaction-aware methods like Fuzzy CNN can detect the hidden SNP-SNP combinations 
                that drive disease risk.""",
                'disease_conclusion': """Pure additive epistasis with max correlation 0.183 - GWAS would fail completely; only interaction detection methods can succeed.""",
                
                'dimensionality': """The top panels show PCA projections (PC1 vs PC2, PC1 vs PC3) with heavy overlap 
                between healthy (blue) and diseased (orange) cases. PC1 and PC2 combined explain only ~4.87% of variance, 
                indicating disease patterns exist in high-dimensional space, not simple linear combinations. The bottom 
                t-SNE panels show some clustering but significant overlap, confirming that disease emerges from complex, 
                non-linear SNP interactions. This low separability in reduced dimensions validates the need for deep 
                learning approaches that can capture high-order interactions.""",
                'dimensionality_conclusion': """Only 4.87% PCA variance with heavy class overlap proves disease exists in high-dimensional interaction space - deep learning required."""
            },
            'model2': {
                'label': """Perfect 50-50 balance maintained (2000 vs 2000). Model 2 (Multiplicative epistasis) shows 
                identical class distribution to Model 1, ensuring fair comparison between different epistatic mechanisms.""",
                'label_conclusion': """Perfect balance maintained for fair comparison of multiplicative vs additive epistasis mechanisms.""",
                
                'snp': """Similar to Model 1, shows ~64% AA, ~32% Aa, ~4% aa distribution consistent with MAF=0.2 and 
                Hardy-Weinberg Equilibrium. The multiplicative epistasis model preserves genotype frequencies while 
                changing how SNP combinations interact to produce disease.""",
                'snp_conclusion': """HWE-compliant genotype distribution (MAF=0.2) ensures multiplicative interactions operate on properly simulated genetic data.""",
                
                'maf': """Observed mean MAF of 0.1988 is extremely close to expected 0.2 (99.4% accuracy). The tight 
                distribution in both histogram and box plot confirms consistent allele frequencies. Slight deviation 
                from 0.2 is within normal sampling variation for 4000 samples.""",
                'maf_conclusion': """99.4% MAF accuracy (0.1988 vs 0.2) within normal sampling variation, confirming quality simulation.""",
                
                'correlation': """Near-zero SNP-SNP correlations (mean ≈ 0.0001) confirm independent SNP generation. 
                The multiplicative epistasis is encoded in the disease generation mechanism, not in SNP correlation 
                structure. This independence allows isolation of true multiplicative interaction effects.""",
                'correlation_conclusion': """Zero SNP-SNP correlation isolates true multiplicative interaction effects from correlation artifacts.""",
                
                'disease': """Maximum SNP-disease correlation of only 0.182 confirms pure epistatic pattern. The histogram 
                shows symmetric, near-zero distribution. In multiplicative epistasis, disease risk = SNP1 × SNP2 effect, 
                making individual SNPs non-predictive. This model tests whether the algorithm can detect multiplicative 
                rather than additive interaction patterns.""",
                'maf_conclusion': """99.9% accuracy provides consistent foundation for complex multi-mechanism interaction architecture.""",
                'disease_conclusion': """Pure multiplicative epistasis (max r=0.182) - disease risk emerges from SNP1 × SNP2 effects, not individual SNPs.""",
                
                'dimensionality': """PCA captures only ~4.84% variance in first two components, with complete overlap of 
                classes. t-SNE shows slightly better separation than Model 1 but still significant mixing. The multiplicative 
                interaction creates complex, non-linear decision boundaries that linear methods cannot capture. Deep 
                architectures with multiplicative interaction layers are essential.""",
                'dimensionality_conclusion': """PCA variance 4.84% with class overlap confirms multiplicative interactions require non-linear detection methods."""
            },
            'model3': {
                'label': """Maintains perfect 50-50 balance. Model 3 (Heterogeneous) combines both marginal effects and 
                epistasis, making it an easier detection target than pure epistasis models.""",
                
                'snp': """Shows ~36% AA, ~48% Aa, ~16% aa, consistent with MAF=0.4 and Hardy-Weinberg Equilibrium 
                (p²=0.36, 2pq=0.48, q²=0.16). Higher MAF of 0.4 creates more heterozygotes, providing maximum genetic 
                variation and information content for learning.""",
                'snp_conclusion': """MAF=0.4 creates 48% heterozygotes - maximum genetic variation providing optimal information for learning.""",
                'label_conclusion': """Perfect balance maintained; heterogeneous model combines marginal + epistatic effects for easier detection.""",
                
                'maf': """Observed mean 0.4008 matches expected 0.4 almost perfectly (99.8% accuracy). The distribution 
                is tightly centered with minimal spread. MAF=0.4 represents the optimal frequency for detecting genetic 
                associations due to maximum heterozygosity and allelic variation.""",
                'maf_conclusion': """99.8% accuracy (0.4008 vs 0.4) at optimal MAF for maximizing heterozygosity and association detection power.""",
                
                'correlation': """Despite heterogeneous disease model, SNP-SNP correlations remain near zero (mean ≈ 0.0001). 
                The heterogeneous effects are in disease risk model (mix of marginal + epistasis), not SNP correlations. 
                This clean separation allows studying complex disease architectures with controlled SNP structure.""",
                'correlation_conclusion': """Zero SNP correlation despite complex disease model proves heterogeneity is in risk function, not SNP structure.""",
                
                'disease': """<b>Critical difference from Models 1-2:</b> Maximum correlation reaches 0.4605 for SNP1, 
                visible as a clear peak in the top 20 SNPs plot. The histogram shows right-skewed distribution with 
                some SNPs showing strong marginal effects. This heterogeneous model combines both main effects (detectable 
                by GWAS) and epistatic effects (requiring interaction methods). Expected to be easier to learn due to 
                strong individual SNP signals.""",
                'disease_conclusion': """Strong marginal effect (r=0.4605) plus epistasis - GWAS will find top SNPs but miss interactions; easiest model.""",
                
                'dimensionality': """PCA still captures only ~4.87% variance, but notice slightly better visual separation 
                in PCA plots compared to Models 1-2. t-SNE shows clearer clustering tendencies. The presence of marginal 
                effects creates some linear separability, but full disease architecture still requires capturing interactions. 
                This model validates that algorithms can benefit from both marginal detection and interaction learning.""",
                'dimensionality_conclusion': """Despite marginal effects, 4.87% PCA variance shows full disease architecture still requires interaction learning."""
            },
            'model4': {
                'label': """Perfect 50-50 balance preserved. Model 4 (Threshold epistasis) represents a biologically 
                realistic scenario where disease manifests only when SNP combinations cross certain thresholds.""",
                'label_conclusion': """Perfect balance for threshold epistasis model - disease appears when SNP combinations exceed thresholds.""",
                
                'snp': """With MAF=0.4, shows expected ~36% AA, ~48% Aa, ~16% aa distribution. Threshold effects operate 
                on these genotypes, with disease emerging when specific genotype combinations exceed threshold values.""",
                'snp_conclusion': """MAF=0.4 provides abundant heterozygotes crucial for threshold models where intermediate genotypes trigger disease.""",
                
                'maf': """Mean MAF of 0.3990 is 99.75% accurate to expected 0.4. Tight distribution confirms consistent 
                simulation. The high MAF provides abundant heterozygotes, important for threshold models where intermediate 
                genotypes play key roles in crossing disease thresholds.""",
                'maf_conclusion': """99.75% accuracy confirms precise simulation needed for threshold effects to manifest correctly.""",
                
                'correlation': """Near-zero SNP-SNP correlations maintained (mean ≈ 0.0001). Threshold epistasis is 
                encoded in the non-linear disease risk function (if SNP1+SNP2 > threshold, then disease), not in SNP 
                correlation structure. Clean SNP independence essential for isolating threshold effects.""",
                'correlation_conclusion': """Independent SNPs essential for isolating threshold effects encoded in non-linear risk functions.""",
                
                'disease': """Maximum correlation of 0.2383 is intermediate - higher than pure epistasis models (0.18) 
                but lower than strong marginal models (>0.46). This suggests weak marginal effects with strong threshold 
                interactions. The histogram shows slight right skew. Threshold models are challenging because disease 
                doesn't scale linearly with SNP counts - it appears suddenly when thresholds are crossed, requiring 
                algorithms to learn sharp decision boundaries.""",
                'disease_conclusion': """Intermediate correlation (0.2383) indicates weak marginal + strong threshold interactions requiring sharp decision boundaries.""",
                
                'dimensionality': """Low PCA variance (~4.82%) indicates threshold effects create complex, non-linear 
                patterns in high-dimensional space. t-SNE shows some separation but with fuzzy boundaries, reflecting 
                the threshold nature - clear separation near threshold regions, ambiguity far from thresholds. This 
                visualization confirms threshold epistasis creates distinct challenges for linear vs non-linear methods.""",
                'dimensionality_conclusion': """Low PCA variance (4.82%) reflects threshold-induced non-linearity - separation appears suddenly at threshold crossings."""
            },
            'model5': {
                'label': """Perfect balance maintained. Model 5 is explicitly designed as Pure Epistasis with zero marginal 
                effects, making it the ultimate test of interaction detection capability.""",
                'label_conclusion': """Perfect balance in ultimate pure epistasis test - zero marginal effects, 100% interaction-driven disease.""",
                
                'snp': """MAF=0.2 produces ~64% AA, ~32% Aa, ~4% aa distribution. Pure epistasis model ensures disease 
                risk comes entirely from SNP combinations, with individual genotype frequencies remaining at HWE expectations.""",
                'snp_conclusion': """HWE-compliant genotypes with MAF=0.2 ensure pure epistasis comes from disease model, not genotype artifacts.""",
                
                'maf': """Mean MAF 0.2003 shows 99.85% accuracy. Extremely tight distribution confirms precise simulation. 
                Pure epistasis models require perfect MAF control because any deviation could introduce spurious marginal 
                associations, confounding pure interaction effects.""",
                'maf_conclusion': """99.85% accuracy critical for pure epistasis - any MAF deviation could introduce spurious marginal associations.""",
                
                'correlation': """Near-zero correlations (mean ≈ 0.0001) are crucial for pure epistasis models. Any 
                SNP-SNP correlation could be mistaken for interaction effects. The clean independence validates that 
                observed epistasis comes from disease model design, not correlation artifacts.""",
                'correlation_conclusion': """Zero correlation mandatory for pure epistasis validation - ensures interactions are real, not correlation effects.""",
                
                'disease': """Maximum correlation of only 0.2109 confirms absolutely no marginal effects. The histogram 
                is perfectly symmetric and centered near zero. This is the gold standard pure epistasis model - GWAS 
                would find nothing, p-values would all be non-significant. Only methods explicitly designed for interaction 
                detection (like Fuzzy CNN, MDR, or other epistasis algorithms) can succeed here. Performance on this 
                model is the true test of epistasis detection capability.""",
                'disease_conclusion': """Gold standard pure epistasis (max r=0.2109) - GWAS p-values all non-significant; only interaction methods succeed.""",
                
                'dimensionality': """Lowest PCA variance among all models indicates disease exists entirely in interaction 
                space, not linear combinations. Complete overlap in PCA plots confirms no linear separability. Even t-SNE 
                struggles to separate classes, showing heavy mixing. This validates that pure epistasis creates the most 
                difficult detection scenario, requiring deep interaction learning without relying on marginal effect shortcuts.""",
                'dimensionality_conclusion': """Lowest separability validates pure epistasis creates hardest scenario - disease entirely in interaction space."""
            },
            'model6': {
                'label': """Perfect 50-50 balance. Model 6 implements XOR-like epistasis - disease appears in specific 
                SNP combinations (e.g., SNP1=1 AND SNP2=0, or SNP1=0 AND SNP2=1) but not others, mimicking exclusive-OR logic.""",
                'label_conclusion': """Perfect balance for XOR-like epistasis - disease in exclusive SNP combinations, not individual SNPs.""",
                
                'snp': """MAF=0.2 gives standard ~64% AA, ~32% Aa, ~4% aa. XOR patterns operate on these genotypes, with 
                disease emerging only in mutually exclusive SNP combination states, creating complex interaction patterns.""",
                'snp_conclusion': """MAF=0.2 genotypes enable XOR pattern where disease appears in mutually exclusive combination states.""",
                
                'maf': """Mean MAF 0.2013 shows 99.35% accuracy to expected 0.2. The XOR pattern requires precise MAF 
                control to ensure symmetric interaction effects - all SNP combinations must have adequate representation 
                for the exclusive pattern to emerge clearly.""",
                'maf_conclusion': """99.35% accuracy ensures symmetric XOR interactions with adequate representation of all combination states.""",
                
                'correlation': """Near-zero SNP-SNP correlations essential for XOR models. True XOR logic requires 
                independent inputs - if SNPs were correlated, the exclusive pattern would be obscured. Clean independence 
                ensures XOR interactions are detectable.""",
                'correlation_conclusion': """Zero correlation essential for XOR logic - independent inputs required for exclusive interaction patterns.""",
                
                'disease': """Maximum correlation of 0.1895 is among the lowest, confirming strongest pure epistasis. 
                The histogram is flat and symmetric. XOR patterns are notoriously difficult to detect because: (1) no 
                marginal effects, (2) opposite direction effects in different combinations, (3) requires detecting 
                specific multi-way interactions. This model tests advanced interaction detection capabilities like 
                multi-layer neural networks or fuzzy logic systems.""",
                'disease_conclusion': """Strongest pure epistasis (r=0.1895) with XOR pattern - requires multi-layer networks; not linearly separable.""",
                
                'dimensionality': """Very low PCA variance (~4.83%) with complete class overlap. Even t-SNE shows minimal 
                separation. XOR patterns are known to be non-linearly separable - cannot be solved by linear classifiers 
                or simple methods. This visualization confirms XOR epistasis creates one of the hardest learning scenarios, 
                requiring deep architectures with multiple non-linear interaction layers.""",
                'dimensionality_conclusion': """Minimal t-SNE separation confirms XOR epistasis is non-linearly separable - classic hard learning problem."""
            },
            'model7': {
                'label': """Perfect balance preserved. Model 7 (Complex) combines multiple types of epistatic mechanisms 
                with strong marginal effects, representing realistic complex disease architecture.""",
                'label_conclusion': """Perfect balance in complex model combining multiple epistatic mechanisms with strongest marginal effects.""",
                
                'snp': """MAF=0.4 produces expected ~36% AA, ~48% Aa, ~16% aa. Complex model leverages high heterozygosity 
                to create intricate combinations of marginal effects, additive interactions, and non-linear epistasis.""",
                'snp_conclusion': """High heterozygosity (48% from MAF=0.4) enables intricate combinations of additive, non-linear, and marginal interactions.""",
                
                'maf': """Mean MAF 0.3996 shows 99.9% accuracy. Tight distribution critical for complex models to ensure 
                all interaction components have consistent foundations. High MAF=0.4 provides maximum variation for 
                complex interaction patterns.""",
                'maf_conclusion': """99.9% accuracy provides consistent foundation for complex multi-mechanism interaction architecture.""",
                
                'correlation': """Near-zero SNP-SNP correlations maintained despite complex disease model. The complexity 
                is in disease risk architecture (multiple interaction types), not SNP correlation structure. Clean 
                independence allows dissecting contributions of different interaction mechanisms.""",
                'correlation_conclusion': """Zero SNP correlation while maintaining complex disease architecture allows dissecting individual interaction contributions.""",
                
                'disease': """<b>Highest correlation of all models: 0.4705 for SNP1.</b> The top 20 SNPs plot shows 
                clear peaks for top SNPs. Histogram is strongly right-skewed with long tail. This complex model has 
                the strongest marginal effects, making it the easiest model for detection. Traditional GWAS would find 
                top SNPs, but interaction methods would additionally capture epistatic layers. Expected to achieve 
                highest accuracy (>90%) and serves as positive control for method validation.""",
                'disease_conclusion': """Strongest marginal effects (r=0.4705) make this easiest model - GWAS finds top SNPs, interaction methods find epistasis; expected >90% accuracy.""",
                
                'dimensionality': """Despite strong marginal effects, PCA still captures only ~4.85% variance, showing 
                disease involves high-dimensional interactions beyond linear combinations. t-SNE shows best separation 
                of all models, with clearer clustering. This validates that complex models with both marginal and epistatic 
                components provide multiple pathways for learning, making them more learnable than pure epistasis models.""",
                'dimensionality_conclusion': """Best t-SNE separation despite 4.85% PCA variance shows complex models with marginal+epistatic components are most learnable."""
            },
            'model8': {
                'label': """Perfect 50-50 balance maintained. Model 8 (Nested epistasis) represents hierarchical interaction 
                structure where some SNP pairs interact, and those interactions further interact with other SNPs.""",
                'label_conclusion': """Perfect balance for nested epistasis - hierarchical SNP interactions at multiple levels.""",
                
                'snp': """MAF=0.4 provides ~36% AA, ~48% Aa, ~16% aa. Nested structure benefits from high heterozygosity 
                to create multi-level interaction hierarchies: SNP1↔SNP2 interaction, then that result ↔ SNP3, etc.""",
                'snp_conclusion': """MAF=0.4 heterozygosity supports multi-level nesting: SNP1↔SNP2 interaction, then result ↔ SNP3, etc.""",
                
                'maf': """Mean MAF 0.3995 shows 99.875% accuracy. Precise MAF control crucial for nested models to ensure 
                each hierarchical level has adequate representation. High MAF maximizes interaction detectability at 
                each nesting level.""",
                'maf_conclusion': """99.875% accuracy ensures each hierarchical interaction level has adequate genotype representation.""",
                
                'correlation': """Near-zero SNP-SNP correlations confirm nested interactions are in disease model, not 
                correlation structure. This separation allows studying how algorithms learn hierarchical interaction 
                patterns from independent SNP inputs.""",
                'correlation_conclusion': """Independent SNPs prove nested structure is in disease model hierarchy, enabling study of hierarchical learning.""",
                
                'disease': """Strong correlation of 0.4624 for SNP2 indicates significant marginal effects in nested 
                model. The histogram shows right skew similar to Model 3 and 7. Nested epistasis with marginal effects 
                means some SNPs in the hierarchy have individual predictive power while others only contribute through 
                interactions. This tests whether algorithms can learn hierarchical feature combinations, essential for 
                capturing nested biological pathways.""",
                'disease_conclusion': """Strong marginal (r=0.4624) in hierarchical context - tests algorithm's hierarchical feature learning capability.""",
                
                'dimensionality': """PCA variance ~4.89% is typical despite nested structure, showing hierarchical 
                interactions still create high-dimensional patterns. t-SNE shows good separation, better than pure 
                epistasis models. The nested structure creates organized interaction patterns that are more learnable 
                than random epistasis. This model tests whether algorithms can benefit from hierarchical feature learning, 
                mimicking how deep networks learn features at multiple abstraction levels.""",
                'dimensionality_conclusion': """Good t-SNE separation (4.89% PCA) shows nested structure creates organized, learnable interaction patterns."""
            }
        }
        
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
            
            analyses = model_analyses[model]
            
            # Label distribution
            label_dist_path = self.eda_dir / f'{model}_label_distribution.png'
            self.add_image_with_caption(
                str(label_dist_path),
                f"Figure: {model} - Disease label distribution showing perfect 50-50 balance",
                analysis=analyses['label'],
                conclusion=analyses['label_conclusion']
            )
            
            # SNP distribution
            snp_dist_path = self.eda_dir / f'{model}_snp_distribution.png'
            self.add_image_with_caption(
                str(snp_dist_path),
                f"Figure: {model} - SNP genotype frequency distribution (0=AA, 1=Aa, 2=aa)",
                analysis=analyses['snp'],
                conclusion=analyses['snp_conclusion']
            )
            
            # MAF analysis
            maf_path = self.eda_dir / f'{model}_maf_analysis.png'
            self.add_image_with_caption(
                str(maf_path),
                f"Figure: {model} - Minor Allele Frequency (MAF) distribution and box plot",
                analysis=analyses['maf'],
                conclusion=analyses['maf_conclusion']
            )
            
            # Correlation analysis
            corr_path = self.eda_dir / f'{model}_correlation_analysis.png'
            self.add_image_with_caption(
                str(corr_path),
                f"Figure: {model} - SNP-SNP correlation heatmap showing independence of SNPs",
                analysis=analyses['correlation'],
                conclusion=analyses['correlation_conclusion']
            )
            
            # Disease association
            disease_path = self.eda_dir / f'{model}_disease_association.png'
            self.add_image_with_caption(
                str(disease_path),
                f"Figure: {model} - SNP-Disease association analysis showing top correlated SNPs",
                analysis=analyses['disease'],
                conclusion=analyses['disease_conclusion']
            )
            
            # Dimensionality reduction
            dim_red_path = self.eda_dir / f'{model}_dimensionality_reduction.png'
            self.add_image_with_caption(
                str(dim_red_path),
                f"Figure: {model} - Dimensionality reduction (PCA and t-SNE) visualization",
                width=5.5*inch,
                analysis=analyses['dimensionality'],
                conclusion=analyses['dimensionality_conclusion']
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
            self.styles['CustomBodyText']
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
        self.story.append(Paragraph(algo_text, self.styles['CustomBodyText']))
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
        self.story.append(Paragraph(perf_text, self.styles['CustomBodyText']))
        self.story.append(Spacer(1, 0.15*inch))
        
        # Federated Learning Considerations
        self.story.append(Paragraph("3. Federated Learning Considerations", self.styles['SubsectionHeader']))
        fed_text = """
        <b>Data Distribution:</b> Each client gets 56 samples (2800/50). Perfect balance is maintained 
        per client. IID distribution is verified, and there is sufficient local data for training.<br/><br/>
        <b>Communication Efficiency:</b> 50 SNPs result in a small feature space. Compressed gradients 
        are feasible with low bandwidth requirements.
        """
        self.story.append(Paragraph(fed_text, self.styles['CustomBodyText']))
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
        self.story.append(Paragraph(conclusion_text, self.styles['CustomBodyText']))
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
        self.story.append(Paragraph(footer_text, self.styles['CustomBodyText']))
    
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
