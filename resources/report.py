from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, KeepTogether
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import date


class Report:
    def __init__(self, course, user):
        self.course = course
        self.user = user

    def __repr__(self):
        return "<Report >"

    def save_pdf(self):
        doc = SimpleDocTemplate("output/AD_BeyondCompliance_{}{}_{}.pdf".format(self.user.firstname, self.user.lastname, self.user.iein), pagesize=letter,
                                rightMargin=36,leftMargin=36,
                                topMargin=55,bottomMargin=40)

        Story = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        logo = "static/img/BeyondComplianceAdminAcademyStorylineLogoHighRes.gif"
        titletext = "IMPLEMENTATION AND DISSEMINATION FORM"
        directionstext = "Directions:<br /><br />Part 1: Reflect upon your observation practice and ways to expand upon it by answering the following questions asked during this academy.<br /><br />Parts 2a and 2b: Create an action plan using what you have learned during this academy to expand your role as a collaborative, supportive evaluator to impact student achievement and professional growth (in yourself and your teachers). Create a progress monitoring plan to measure progress on your actions."
        part1text = "Part 1: Reflecting on Your Current Observation Practices and Planning Improvements"
        part2atext = "Part 2: A) Determine an Action Plan to improve upon observation practices and impact Student Achievement and Professional Growth"
        part2btitletext = "Part 2: B) Check on Progress"
        part2bbodytext = "Based on the action plan from above, check your progress toward improvement after a short period of time."

        im = Image(logo, 2 * inch, 0.84 * inch)
        Story.append(im)

        title = '<font size=12>%s</font>' % titletext
        Story.append(Paragraph(title, styles["Title"]))

        directions = '<font size=10>%s</font>' % directionstext
        Story.append(Paragraph(directions, styles["Normal"]))

        part1 = '<font size=12>%s</font>' % part1text
        Story.append(Paragraph(part1, styles["Heading2"]))

        question1atext = '<strong>1a) In what ways do you capture evidence of teacher planning during the pre/post conversations and observations?</strong>'
        question1btext = '<strong>1b) How will you encourage and support teachers in being reflective about their practice?</strong>'
        question1ctext = '<strong>1c) What will you do to ensure the evidence you collect is bias & interpretation free?</strong>'
        question1dtext = '<strong>1d) Thinking back on what was presented during this academy, what has been confirming for you about the observation practices you use (pre/post conversations and observations)?</strong>'
        question1etext = '<strong>1e) What are some practices you might discontinue (for pre/post conversations and observations)?</strong>'
        question1ftext = '<strong>1f) What are new ideas you will implement for pre/post conversations and observations to improve and expand your observation practice?</strong>'

        part1data = []
        for interaction in sorted(self.course.interactions, key=lambda x: x.id if x.id else 'interactions_1000'):
            if interaction.slide_id == 'Scene1_Slide19_Essay_0_0':
                part1data.append([Paragraph(question1atext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.slide_id == 'Scene1_Slide20_Essay_0_0':
                part1data.append([Paragraph(question1btext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.slide_id == 'Scene1_Slide21_Essay_0_0':
                part1data.append([Paragraph(question1ctext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.slide_id == 'Scene1_Slide22_Essay_0_0':
                part1data.append([Paragraph(question1dtext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.slide_id == 'Scene1_Slide23_Essay_0_0':
                part1data.append([Paragraph(question1etext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])
            if interaction.slide_id == 'Scene1_Slide24_Essay_0_0':
                part1data.append([Paragraph(question1ftext, styles["Normal"]),
                                  Paragraph(interaction.student_response, styles["Normal"])])

        t = Table(part1data, [3.6*inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ]))

        Story.append(t)

        part2a = '<font size=12>%s</font>' % part2atext
        # Story.append(Paragraph(part2a, styles["Heading2"]))

        part2adata = [[
            Paragraph('Action Step', styles["Heading4"]),
            Paragraph('Timeline', styles["Heading4"]),
            Paragraph('Resources', styles["Heading4"])
        ]]
        outcomes = []
        for interaction in self.course.interactions:
            # print(interaction.id)
            # print(interaction.student_response)
            if interaction.slide_id == 'Scene1_Slide25_Essay_0_0':
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
                        # print(row_array)
                        if not all(cell is '' for cell in row_array):
                            part2adata.append([Paragraph(cell, styles["Normal"]) for cell in row_array])
                    i += 1
                # Story.append(Paragraph(interaction.student_response, styles["Normal"]))

        # print(outcomes)
        part2adata.append([Paragraph('<strong>Expected Outcomes:</strong><br />{}'.format("<br />".join(outcomes)), styles["Normal"])])

        t = Table(part2adata, [2.4 * inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('SPAN', (0, len(part2adata) - 1), (2, len(part2adata) - 1))
                               ]))

        # print(len(part2adata))

        part2a = [Paragraph(part2a, styles["Heading2"])]
        part2a.append(t)
        Story.append(KeepTogether(part2a))

        part2btitle = '<font size=12>%s</font>' % part2btitletext
        part2bbody = '<font size=12>%s</font>' % part2bbodytext

        # Story.append(Paragraph(part2btitle, styles["Heading2"]))
        # Story.append(Paragraph(part2bbody, styles["Normal"]))

        # Story.append(Spacer(1, 12))

        progress_date_answer = None
        for interaction in self.course.interactions:
            if interaction.slide_id == 'Scene1_Slide26_Essay_0_0':
                progress_date_answer = interaction.student_response

        part2bdata = [
            [Paragraph('<strong>Establish a progress check date and metrics for your Action Plan</strong>', styles["Normal"]), Paragraph(progress_date_answer, styles["Normal"])],
            ['--questions below to be answered at the established progress check date--'],
            [Paragraph('<strong>Describe what progress has been made thus far.</strong>', styles["Normal"]), Paragraph('<br /><br /><br /><br />', styles["Normal"])],
            [Paragraph('<strong>What might be the “Next Steps” towards either attainment of the goal or establishing a new goal?</strong>', styles["Normal"]), Paragraph('<br /><br /><br /><br />', styles["Normal"])],
            [Paragraph('<strong>What supports or resources are needed at this check point?</strong>',styles["Normal"]), Paragraph('<br /><br /><br /><br />', styles["Normal"])],
        ]

        t = Table(part2bdata, colWidths=[3.6 * inch])
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('SPAN', (0, 1), (1, 1)),
                               ('ALIGN', (0, 1), (1, 1), 'CENTER'),
                               ]))

        part2b = [Paragraph(part2btitle, styles["Heading2"])]
        part2b.append(Paragraph(part2bbody, styles["Normal"]))
        part2b.append(Spacer(1, 12))
        part2b.append(t)

        Story.append(KeepTogether(part2b))

        doc.build(Story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

    def _header_footer(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('Participant: {} {}, IEIN: {}'.format(self.user.firstname, self.user.lastname, self.user.iein), styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('© {} Consortium for Education Change. All rights reserved.'.format(date.today().year), styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h + 16)

        # Release the canvas
        canvas.restoreState()