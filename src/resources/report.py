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
        self.name = None

    def __repr__(self):
        return "<Report {} {}>".format(self.course.name, self.user.email)

    def _generate_report_content(self):
        pass  # either modify this or create a subclass for each report type and override this method there

    def save_pdf(self):
        doc = SimpleDocTemplate(
            "output/{}/{}".format(self.output_subdir, self.name),
            pagesize=letter,
            rightMargin=36, leftMargin=36,
            topMargin=55, bottomMargin=40)
        Story = self._generate_report_content()
        doc.build(Story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

    def save_multiple_as_pdf(self):
        pass

    def _header_footer(self, canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        try:
            header = Paragraph('Participant: {} {}, IEIN: {}, AA #1803'.format(self.user.firstname, self.user.lastname,
                                                                               self.user.iein), styles['Normal'])
        except AttributeError:
            header = Paragraph('AA #1803', styles['Normal'])

        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('© {} Consortium for Education Change. All rights reserved.'.format(date.today().year), styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h + 16)

        # Release the canvas
        canvas.restoreState()

    @staticmethod
    def _interpret_likert(likert):
        qa_list = []
        i = 1
        for qa in likert.split('___'):
            qa_cleaned = qa.replace('__', ', ').replace('_', ' ')
            if i % 2 == 0: # even, i.e. answer
                new_qa.append(qa_cleaned)
                qa_list.append(new_qa)
            else: # odd, i.e. question
                new_qa = [qa_cleaned]
            i += 1
        # print(qa_list)
        return qa_list

    @staticmethod
    def _format_qa_pairs_for_table_display(qa_pairs):
        styles = getSampleStyleSheet()
        new_qa_pairs = []
        for qa_pair in qa_pairs:
            new_qa_pairs.append([Paragraph('<strong>{}</strong>'.format(qa_pair[0]), styles["Normal"]), Paragraph(qa_pair[1], styles["Normal"])])
        return new_qa_pairs
