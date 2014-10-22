# -*- coding: utf-8 -*-
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4,landscape
from reportlab.platypus import Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

from django.conf import settings


CURRENT_DIR = os.path.realpath(os.path.dirname(__file__))
FONT_FILE = os.path.join(CURRENT_DIR, 'Arial.ttf')
pdfmetrics.registerFont(TTFont("Arial", FONT_FILE)) 

### Variables ###


width,height=landscape(A4) # width and height of A4 Landscape format

marginX,marginY=0,0

titleX,titleY=3.57*cm+100,9.95*cm+100

nameX,nameY=2.17*cm+100,7.71*cm+100

mainContentX,mainContentY=2.17*cm+100,7.04*cm+100

dateX,dateY=2.17*cm+100,3.74*cm+100

legalMentionsX,legalMentionsY=2.17*cm+100,0.8*cm+100

logoX,logoY=2.17*cm+100,11.6*cm+100

logoOrganizationX,logoOrganizationY=18*cm+100,11.6*cm+100

listProfessorsX,listProfessorsY=width-150,height-190

URLFunX,URLFunY=100+7.57*cm,2.25*cm+100

MoocX,MoocY=2.17*cm+100,1.47*cm+100

#################

class CertificateInfo(object):
    full_name = ""
    course_name = ""
    organization = ""
    organization_logo = ""
    pdf_file_name = ""
    teachers = []
    organizationNameTooLong=False
    courseNameTooLong=False


    def generate(self):
        c=canvas.Canvas(self.pdf_file_name,pagesize=landscape(A4))


        if len(self.organization)>33:
            self.organizationNameTooLong=True

        if len(self.course_name)>33:
            self.courseNameTooLong=True

        #border
        c.setStrokeColorRGB(221./256,221./256,221./256)
        c.setLineWidth(cm*0.13)
        c.rect(100,100,cm*23.84,cm*15)


        #title
        textobject=c.beginText()
        textobject.setTextOrigin(titleX,titleY)
        textobject.setFont("Arial",24)
        textobject.setFillColorRGB(59./256,118./256,188./256)
        textobject.textLine(u" ATTESTATION DE SUIVI AVEC SUCCÈS")
        c.drawText(textobject) 

        c.setFillColorRGB(221./256,221./256,221./256)
        if (self.organizationNameTooLong):
            if (self.courseNameTooLong):
                c.rect(100,2.43*cm+100,400,6.41*cm,fill=1,stroke=0)
                c.rect(cm*22.6+100,2.43*cm+100,1.24*cm,6.41*cm,fill=1,stroke=0)
            else:
                c.rect(100,2.73*cm+100,400,6.11*cm,fill=1,stroke=0)
                c.rect(cm*22.6+100,2.73*cm+100,1.24*cm,6.11*cm,fill=1,stroke=0)
        else:
            c.rect(100,3.23*cm+100,400,5.61*cm,fill=1,stroke=0)
            c.rect(cm*22.6+100,3.23*cm+100,1.24*cm,5.61*cm,fill=1,stroke=0)


        #Name
        textobject=c.beginText()
        textobject.setTextOrigin(nameX,nameY)
        textobject.setFont("Arial",24)
        textobject.setFillColorRGB(0,0,0)
        textobject.textLine(self.full_name)
        c.drawText(textobject)


        #Main Content
        textobject=c.beginText()
        textobject.setTextOrigin(mainContentX,mainContentY)
        textobject.setFont("Arial",16)
        textobject.setFillColorRGB(127./256,127./256,127./256)
        textobject.textOut(u"a suivi avec succès le MOOC")
        textobject.setFillColorRGB(59./256,118./256,188./256)
        textobject.textLine("*")


        textobject.setFillColorRGB(0,0,0)
        textobject.moveCursor(0,10)
        if (self.courseNameTooLong):
            indexReturnLine=self.course_name.rfind(" ",0,43)
            textobject.textLine(self.course_name[:indexReturnLine])
            textobject.textLine(self.course_name[indexReturnLine+1:])
        else:
            textobject.textLine(self.course_name)

        textobject.setFillColorRGB(127./256,127./256,127./256)
        if (self.organizationNameTooLong):
            indexReturnLine=self.organization.rfind(" ",0,33)
            textobject.textOut(u"proposé par ")
            textobject.setFillColorRGB(0,0,0)
            textobject.textLine(self.organization[:indexReturnLine])
            textobject.textLine(self.organization[indexReturnLine+1:])
        else:
            textobject.textOut(u"proposé par ")
            textobject.setFillColorRGB(0,0,0)
            textobject.textLine(self.organization)
        textobject.setFillColorRGB(0,0,0)

        textobject.setFillColorRGB(127./256,127./256,127./256)
        textobject.textOut(u"et diffusé sur la ")
        textobject.setFillColorRGB(0,0,0)
        textobject.textLine(u"plateforme FUN")
        textobject.setFillColorRGB(59./256,118./256,188./256)
        textobject.textLine(datetime.date.today().strftime('Le %d/%m/%Y'))
        c.drawText(textobject)


        #legal mentions
        textobject=c.beginText()
        textobject.setTextOrigin(legalMentionsX,legalMentionsY)
        textobject.setFont("Arial",8.5)
        textobject.setFillColorRGB(0,0,0)
        legalMentions=u"La présente attestation n’est pas un diplôme et ne confère pas de crédits (ECTS). Elle n'atteste pas que le participant était inscrit à/au {}.".format(self.organization)
        if (len(legalMentions)>169):
            indexReturnLine=legalMentions.rfind(" ",0,169)
            textobject.textLine(legalMentions[:indexReturnLine])
            textobject.textOut(legalMentions[indexReturnLine+1:])
            textobject.textLine(u". L’identité du participant n’a pas été vérifiée.")
        else:
            textobject.textLine(u"La présente attestation n’est pas un diplôme et ne confère pas de crédits (ECTS). Elle n'atteste pas que le participant était inscrit à/au {}.".format(self.organization))
            textobject.textLine(u"L’identité du participant n’a pas été vérifiée.")
        c.drawText(textobject)
     
        #logo of FUN
        c.drawImage(settings.FUN_LOGO_PATH,logoX,logoY,width=83,height=77,mask='auto')


        #logo of the organization
        if (self.organization_logo):
            c.drawImage(self.organization_logo,logoOrganizationX,logoOrganizationY,width=140,height=80,mask='auto')


        #List of professors
        c.setFont("Arial",16)
        c.setFillColorRGB(59./256,118./256,188./256)
        c.drawRightString(100+21.70*cm,100+8.40*cm,"Les enseignants")
        y=7.5
        c.setFillColorRGB(0,0,0)
        c.setFont("Arial",12)
        for teacher in self.teachers:
            teacherNameAndJob=teacher.split("/")
            teacherName=teacherNameAndJob[0]
            teacherJob=teacherNameAndJob[1]
            c.setFillColorRGB(0,0,0)
            c.drawRightString(100+21.70*cm,100+y*cm,teacherName)
            c.setFillColorRGB(127./256,127./256,127./256)
            c.drawRightString(100+21.70*cm,100+(y-0.53)*cm,teacherJob)
            y=y-1.24



        #URL Fun
        textobject=c.beginText()
        if (self.organizationNameTooLong):
            textobject.setTextOrigin(URLFunX,URLFunY-10)
        else:
            textobject.setTextOrigin(URLFunX,URLFunY)
        textobject.setFont("Arial",12)
        textobject.setFillColorRGB(59./256,118./256,188./256)
        textobject.textLine(u"http://www.france-universite-numerique-mooc.fr")
        c.drawText(textobject)   


	    #Mooc : cours en ligne
        textobject=c.beginText()
        textobject.setTextOrigin(MoocX,MoocY)
        textobject.setFont("Arial",8)
        textobject.setFillColorRGB(59./256,118./256,188./256)
        textobject.textOut("* ")
        textobject.setFillColorRGB(127./256,127./256,127./256)
        textobject.textLine(u"MOOC : cours en ligne")
        c.drawText(textobject) 	 



        c.showPage()
        c.save()

        return True
