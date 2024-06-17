from typing import Literal
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .session_instance import Session

from ..models import (
	Teacher,
	Student
)

from ..forms import (
	FormStatus,
	edit_profile_form
)

from ..common_solves import (
	check_auth
)

session = Session().session


def welcome(request: HttpRequest) -> HttpResponse:
	class User():
		def __init__(
			self,
			user_type: Literal["teacher", "student"],
			user_id: int,
			user_instance: Teacher | Student
		):
			self.user_type = user_type
			self.user_id = user_id
			self.name = user_instance.name
			self.surname = user_instance.surname
			self.user_model = Teacher if\
				user_type == "teacher" else Student
			self.phone = user_instance.phone if\
				user_type == "teacher" else None
			self.group_id = user_instance.group_id if\
				user_type == "student" else None
		
		def __str__(self) -> str:
			return f"{self.user_type.title()} {self.user_id} {
				self.name} {self.surname}"

		def __bool__(self) -> bool:
			return True if self.user_id else False
		

	user_id = request.POST.get("user_id", None)
	user_type = request.POST.get("user_type", None)
	user_instance: User = None

	if all([user_id, user_type]):
		user_id = int(user_id)
		try:
			if user_type == "teacher":
				user_instance = User(
					user_type="teacher",
					user_id=user_id,
					user_instance=Teacher.objects.get(id=user_id),
				)
			elif user_type == "student":
				user_instance = User(
					user_type="student",
					user_id=user_id,
					user_instance=Student.objects.get(id=user_id),
				)
		except Exception:
			return render(
				request=request,
				template_name="authorisation.html",
				context={
					"user_instance": user_instance,
					"status": FormStatus.DOESNOT_EXIST,
				}
			)

		if user_instance.name:
			session["user_id"] = user_instance.user_id
			session["user_type"] = user_instance.user_type
			session["user_name"] = user_instance.name
			session["user_surname"] = user_instance.surname
			session["student_group_id"] = user_instance.group_id
			session["teacher_phone"] = user_instance.phone
			session.save()

			return redirect(user_type)
	else:
		status = FormStatus.PARTIAL_CONSISTENT\
			if any([user_id, user_type]) else\
				FormStatus.DEFAULT

		return render(
			request=request,
			template_name="authorisation.html",
			context={
				"status": status,
			}
		)


def load_user_page(
	request: HttpRequest,
	user_type: Literal["student", "teacher"]
) -> HttpResponse:
	logged, session_user_instance = check_auth(
		session
	)

	if not logged:
		return redirect("authorisation")

	context={
		"name": session_user_instance["user_name"],
		"surname": session_user_instance["user_surname"],
		"user_type": session_user_instance["user_type"],
		"user_id": session_user_instance["user_id"],
		"group_id": session_user_instance["student_group_id"],
		"phone": session_user_instance["teacher_phone"]
	}

	return render(
		request=request,
		template_name=f"{user_type}.html",
		context=context
	)


def student(
	request: HttpRequest
) -> HttpResponse:
	return load_user_page(
		request=request,
		user_type="student"
	)


def teacher(
	request: HttpRequest
) -> HttpResponse:
	return load_user_page(
		request=request,
		user_type="teacher"
	)


def my_account(
	request: HttpRequest
) -> HttpResponse:
	logged, session_user_instance = check_auth(
		session
	)

	if not logged:
		return redirect("authorisation")

	form = edit_profile_form(
		role=session_user_instance["user_type"],
		# user_id=session_user_instance["user_id"],
		name=session_user_instance["user_name"],
		surname=session_user_instance["user_surname"],
		phone=session_user_instance["teacher_phone"],
		group_id=session_user_instance["student_group_id"],
	)

	return render(
		request=request,
		template_name="my_account.html",
		context={
			"name": session_user_instance["user_name"],
			"surname": session_user_instance["user_surname"],
			"user_type": session_user_instance["user_type"],
			"form": form
		}
	)


def update_user_data(
	request: HttpRequest
) -> HttpResponse:
	is_student = session["user_type"] == "student"

	model = Student if is_student else Teacher

	user = model.objects.get(id=session["user_id"])
	user.name = request.POST.get('name', None)
	user.surname = request.POST.get('surname', None)
	
	session["user_name"] = user.name
	session["user_surname"] = user.surname
	
	if is_student:
		user.group_id = int(request.POST['group'])
		session["student_group_id"] = user.group_id
	else:
		user.phone = request.POST['phone']
		session["teacher_phone"] = user.phone

	user.save()
	session.save()

	return redirect(session["user_type"])


def registration(
	request: HttpRequest
) -> HttpResponse:
	status = FormStatus.DEFAULT

	name = request.POST.get("name", None)
	surname = request.POST.get("surname", None)
	group = request.POST.get("group", None)
	phone = request.POST.get("phone", None)

	if name and surname and (phone or group):
		new_user: Student | Teacher = None

		try:
			if group and not Student.objects.filter(
				name=name, surname=surname, group_id=group
			).exists():
				new_user = Student.objects.create(
					name=name,
					surname=surname,
					group_id=int(group)
				)
			elif phone and not Teacher.objects.filter(
				name=name, surname=surname, phone=phone
			).exists():
				new_user = Teacher.objects.create(
					name=name,
					surname=surname,
					phone=phone
				)
			else:
				return render(
                    request=request,
                    template_name="registration.html",
                    context={
                        "status": FormStatus.ALREADY_EXISTS,
                    }
                )

			session["user_id"] = new_user.pk
			session["user_type"] = "student"\
				if group else "teacher"
			session["user_name"] = new_user.name
			session["user_surname"] = new_user.surname

			if group:
				session["student_group_id"] = new_user.group_id
				session.save()
				return redirect("student")
			else:
				session["teacher_phone"] = new_user.phone
				session.save()
				return redirect("teacher")
		except Exception as ex:
			print(ex)
			status = FormStatus.CREATING_USER_ERROR

	elif any((name, surname, group, phone)):
		status = FormStatus.PARTIAL_CONSISTENT

	return render(
		request=request,
		template_name="registration.html",
		context={
			"status": status,
		}
	)


def logout(
	request: HttpRequest
) -> HttpResponse:
	session.clear()
	return redirect('authorisation')
