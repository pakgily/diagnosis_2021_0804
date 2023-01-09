import os
import numpy as np
import pandas as pd
import win32com.client, sys
from win32com.client import Dispatch

PowerPoint = win32com.client.Dispatch("PowerPoint.Application")
PowerPoint.Visible = True # Background process
PowerPoint.DisplayAlerts = 0  # No display, no warning
# prs = PowerPoint.Presentations.Open(pptx_fpath, ReadOnly= False, WithWindow=False)
Presentation = PowerPoint.Presentations.Add() # 최종 presentation obj Return
Presentation.PageSetup.SlideSize = 0x03 # A4 size로 변경
Presentation.ApplyTheme("C:\\Users\\Administrator\\AppData\\Roaming\\Microsoft\\Templates\\Document Themes\\보고서 자동화_TEST.thmx")

title_layout = Presentation.SlideMaster.CustomLayouts(1) #custom layout for a slide 반환
ct1_layout = Presentation.SlideMaster.CustomLayouts(2)
ct2_layout = Presentation.SlideMaster.CustomLayouts(3)

Presentation.Slides.AddSlide(1,title_layout) #AddSlide의 첫번째 인자 (Slide Index), 두번째 인자는 custom Layout만 들어가야 함.
Presentation.Slides.AddSlide(Presentation.Slides.Count+1,ct1_layout)


shape_index ={}
for i, shape in enumerate(Presentation.Slides(1).Shapes): #enumerate : 리스트의 순서(i)와 리스트 값(shape)을 전달
    shape_index[ shape.name ] = i
print(pd.Series(shape_index))

current_path = os.getcwd().replace('/','\\') + '\\'
add_image = '새로운 표1.jpg'

print(current_path+add_image)
Presentation.Slides(2).Shapes.AddPicture(current_path+add_image, False,True,0,0)
Presentation.SaveAs()