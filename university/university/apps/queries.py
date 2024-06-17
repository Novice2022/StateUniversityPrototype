from django.db.models import Sum

from .models import (
	Schedule,
	Scores,
	Student
)


def get_student_lessons(
	group_id: int
):
	return Schedule.objects.filter(group_id=group_id)\
		.select_related("subject", "teacher", "group").values(
			"subject__name",
			"couple_number",
			"teacher__name",
			"teacher__surname",
			"week_day",
			"calendar_date",
		)

def get_student_marks(
	student_id: int
):
	return Scores.objects.filter(student_id=student_id)\
		.values(
			"subject__name",
			# "subject__lesson_type",
		) \
		.annotate(scores_amount=Sum("scores_amount")) \
		.order_by("subject__name")  # , "subject__lesson_type"


def get_teacher_schedule(
	teacher_id: int
):
	return Schedule.objects.filter(teacher_id=teacher_id)\
		.order_by("calendar_date")\
			.select_related("subject").values(
				"subject__name",
				"subject__lesson_type",
				"couple_number",
				"group_id",
				"week_day",
				"calendar_date",
			)


def get_teacher_groups(
	teacher_id: int
):
	groups_for_teacher = Schedule.objects.filter(
		teacher_id=teacher_id
	).order_by("group").values("group")

	result = []

	for group in groups_for_teacher:
		element_group = group["group"]
		element_students = Student.objects.filter(
			group_id=element_group
		).values(
			"name",
			"surname",
		)

		result.append({
			"group": element_group,
			"students": element_students
		})
	
	return result


def get_student_pie_diagram_data(
	student_id: int
) -> dict[str, int]:
	result = {
		"passed": 0,
		"failed": 0,
	}

	marks = get_student_marks(student_id)

	for mark in marks:
		if int(mark["scores_amount"]) >= 40:
			result["passed"] += 1
		else:
			result["failed"] += 1

	return result


def get_teacher_histogram_data(
	teacher_id: int
) -> dict[str, int]:
	result = {
		"лекция": 0,
		"практика": 0,
		"лабораторная работа": 0,
		"зачёт": 0,
		"курсовая работа": 0,
	}

	for lesson in get_teacher_schedule(teacher_id):
		result[
			lesson["subject__lesson_type"]
		] += 1

	result = {
		"л": result["лекция"],
		"пр": result["практика"],
		"лр": result["лабораторная работа"],
		"зч": result["зачёт"],
		"кр": result["курсовая работа"],
	}

	return result
