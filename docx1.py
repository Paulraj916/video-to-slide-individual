import aspose.slides as slides

# Load presentation
pres = slides.Presentation("output/video.pptx")

# Convert PPTX to PDF
pres.save("pptx-to-pdf.pdf", slides.export.SaveFormat.PDF)