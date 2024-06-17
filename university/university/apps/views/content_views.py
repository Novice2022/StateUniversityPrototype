from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .session_instance import Session
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ..queries import (
	get_student_lessons,
	get_student_marks,
	get_teacher_schedule,
	get_teacher_groups,
	get_student_pie_diagram_data,
	get_teacher_histogram_data,
)

from io import BytesIO
import base64
import json

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

""" Rebuild as partitions pages which upload content via ajax requests """


session = Session().session


@csrf_exempt
@require_http_methods(["POST"])
def student_lessons(
	request: HttpRequest,
) -> HttpResponse:
	return render(
		request=request,
		template_name="student_lessons.html",
		context={
			"schedule": get_student_lessons(
				int(request.POST["group_id"])
			)
		}
	)


@csrf_exempt
@require_http_methods(["POST"])
def student_marks(
	request: HttpRequest,
) -> HttpResponse:
	return render(
		request=request,
		template_name="student_marks.html",
		context={
			"marks": get_student_marks(
				int(request.POST["student_id"])
			)
		}
	)


@csrf_exempt
@require_http_methods(["POST"])
def teacher_schedule(
	request: HttpRequest,
):
	return render(
		request=request,
		template_name="teacher_schedule.html",
		context={
			"schedule": get_teacher_schedule(
				int(request.POST["teacher_id"])
			)
		}
	)


@csrf_exempt
@require_http_methods(["POST"])
def teacher_groups(
	request: HttpRequest,
) -> dict[
	str,
	int | dict[str, str]
]:
	return render(
		request=request,
		template_name="teacher_groups.html",
		context={
			"groups": get_teacher_groups(
				int(request.POST["teacher_id"])
			)
		}
	)


@csrf_exempt
@require_http_methods(["POST"])
def student_diagram(
	request: HttpRequest
) -> HttpResponse:
	content = get_student_pie_diagram_data(
		int(request.POST["student_id"])
	)

	# fig = plt.figure()
	# fig.set_facecolor((19 / 256, 21 / 256, 30 / 256))

	plt.pie(content.values(), labels=content.keys())
	plt.title('Passed/Failed 40 boundary')  # , color=(1, 1, 1)

	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	plt.close()

	image_png = buffer.getvalue()
	buffer.close()
	graphic = base64.b64encode(image_png).decode()

	return HttpResponse('<img src="data:image/png;base64,{}">'.format(graphic))


@csrf_exempt
@require_http_methods(["POST"])
def teacher_diagram(
	request: HttpRequest
) -> HttpResponse:
	content = get_teacher_histogram_data(
		int(request.POST["teacher_id"])
	)

	plt.bar(content.keys(), content.values())
	plt.xticks(range(len(content)), content.keys())
	plt.title('Distribution of types of classes')  # , color=(1, 1, 1)

	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	plt.close()

	image_png = buffer.getvalue()
	buffer.close()
	graphic = base64.b64encode(image_png).decode()

	return HttpResponse('<img src="data:image/png;base64,{}">'.format(graphic))
