from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors


class Report:
    def __init__(self, course, user):
        self.course = course
        self.user = user

    def __repr__(self):
        return "<Report >"

    def save_pdf(self):
        doc = SimpleDocTemplate("output/AD_BeyondCompliance_{}{}_{}.pdf".format(self.user.firstname, self.user.lastname, self.user.iein), pagesize=letter,
                                rightMargin=36,leftMargin=36,
                                topMargin=36,bottomMargin=36)

        Story = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        logo = "static/img/BeyondComplianceAdminAcademyStorylineLogoHighRes.gif"
        titletext = "IMPLEMENTATION AND DISSEMINATION FORM"
        directionstext = "Directions:<br /><br />Part 1: Reflect upon your observation practice and ways to expand upon it by answering the following questions asked during this academy.<br /><br />Parts 2 and 3: Create an action plan using what you have learned during this academy to expand your role as a collaborative, supportive evaluator to impact student achievement and professional growth (in yourself and your teachers). Create a progress monitoring plan to measure progress on your actions."
        part1text = "Part 1: Reflecting on Your Current Observation Practices and Planning Improvements"
        part2atext = "Part 2: A) Determine an Action Plan to improve upon observation practices and impact Student Achievement and Professional Growth"
        part2btext = "Part 2: B) Check on Progress<br />Based on the action plan from above, check your progress toward improvement after a short period of time."

        im = Image(logo, 2 * inch, 0.84 * inch)
        Story.append(im)

        title = '<font size=12>%s</font>' % titletext
        Story.append(Paragraph(title, styles["Title"]))

        directions = '<font size=10>%s</font>' % directionstext
        Story.append(Paragraph(directions, styles["Normal"]))

        part1 = '<font size=12>%s</font>' % part1text
        Story.append(Paragraph(part1, styles["Heading2"]))

        question1atext = '1a) In what ways do you capture evidence of teacher planning during the pre/post conversations and observations?'
        question1btext = '1b) How will you encourage and support teachers in being reflective about their practice?'
        question1ctext = '1c) What will you do to ensure the evidence you collect is bias & interpretation free?'
        question1dtext = '1d) Thinking back on what was presented during this academy, what has been confirming for you about the observation practices you use (pre/post conversations and observations)?'
        question1etext = '1e) What are some practices you might discontinue (for pre/post conversations and observations)?'
        question1ftext = '1f) What are new ideas you will implement for pre/post conversations and observations to improve and expand your observation practice?'

        part1data = []
        for interaction in sorted(self.course.interactions, key=lambda x: x.id if x.id else 'interactions_1000'):
            if interaction.id == 'interactions_4':
                part1data.append([Paragraph(question1atext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.id == 'interactions_5':
                part1data.append([Paragraph(question1btext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.id == 'interactions_6':
                part1data.append([Paragraph(question1ctext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.id == 'interactions_7':
                part1data.append([Paragraph(question1dtext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.id == 'interactions_8':
                part1data.append([Paragraph(question1etext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.id == 'interactions_9':
                part1data.append([Paragraph(question1ftext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])

        t = Table(part1data, [3.6*inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ]))

        Story.append(t)

        part2a = '<font size=12>%s</font>' % part2atext
        Story.append(Paragraph(part2a, styles["Heading2"]))

        part2adata = [[
            Paragraph('Action Step', styles["Heading4"]),
            Paragraph('Timeline', styles["Heading4"]),
            Paragraph('Resources', styles["Heading4"])
        ]]
        outcomes = []
        for interaction in self.course.interactions:
            if interaction.id == 'interactions_10':
                i = 1
                for row in interaction.student_response.split("\r"):
                    if i == 6:
                        row_array = row.split("\t")
                        del row_array[0]
                        outcomes.append(row_array[0])
                    elif i > 6:
                        outcomes.append(row)
                    else:
                        # print(row)
                        row_array = row.split("\t")
                        del row_array[0]
                        part2adata.append([Paragraph(cell, styles["Normal"]) for cell in row_array])
                    i += 1
                # Story.append(Paragraph(interaction.student_response, styles["Normal"]))

        # print(outcomes)
        part2adata.append([Paragraph('<strong>Expected Outcomes:</strong><br />{}'.format("<br />".join(outcomes)), styles["Normal"])])

        t = Table(part2adata, [2.4 * inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('SPAN', (0, 6), (2, 6))
                               ]))
        Story.append(t)

        # Story.append(Spacer(1, 12))

        # part2b = '<font size=12>%s</font>' % part2btext
        # Story.append(Paragraph(part2b, styles["Heading2"]))

        doc.build(Story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

    def _header_footer(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        # header = Paragraph('User: username', styles['Normal'])
        # w, h = header.wrap(doc.width, doc.topMargin)
        # header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('Participant: {} {}, IEIN: {}<br />© Consortium for Education Change 2017. All rights reserved.'.format(self.user.firstname, self.user.lastname, self.user.iein), styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()