import aspose.slides as slides
import aspose.words as words
import glob

presentation = slides.Presentation("output\image.pptx")
doc = words.Document()
builder = words.DocumentBuilder(doc)

for index in range(presentation.slides.length):
    slide = presentation.slides[index]
    # generates and inserts slide image
    slide.get_thumbnail(2,2).save("slide_{i}.png".format(i = index), drawing.imaging.ImageFormat.png)
    builder.insert_image("slide_{i}.png".format(i = index))
    
    for shape in slide.shapes:
        # inserts slide's texts
        if (type(shape) is slides.AutoShape):
            builder.writeln(shape.text_frame.text)
   
    builder.insert_break(words.BreakType.PAGE_BREAK) 
doc.save("presentation.docx")