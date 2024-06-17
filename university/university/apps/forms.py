from dataclasses import dataclass
from typing import Literal

from django import forms

from .models import (
	Teacher,
	Student,
)


@dataclass
class FormStatus:
	DEFAULT = 0
	PARTIAL_CONSISTENT = -1
	DOESNOT_EXIST = -2
	CREATING_USER_ERROR = -3
	ALREADY_EXISTS = -4


def edit_profile_form(
	role: Literal["student", "teacher"],
	# user_id: int,
	name: str,
	surname: str,
	group_id: int,
	phone: str,
) -> dict[str, str]:
	key: str
	value: forms.Field

	if role == "student":
		key = "group"
		value = group_id
	else:
		key = "phone"
		value = phone

	return type(
		"EditProfileForm",
		(forms.Form, ),
		{
			"name": name,
			"surname": surname,
			key: value
		}
	)
