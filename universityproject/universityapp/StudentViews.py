from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
import datetime  # To Parse input DateTime into Python Date Time Object

from universityapp.models import CustomUser, Staffs, Courses, Subjects, Students, StudentResult


def student_home(request):
    student_obj = Students.objects.get(admin=request.user.id)
    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj).count()

    subject_name = []
    subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        subject_name.append(subject.subject_name)

    context = {
        "total_subjects": total_subjects,
        "subject_name": subject_name,

    }
    return render(request, "student_template/student_home_template.html", context)


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context = {
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    student_result = StudentResult.objects.filter(student_id=student.id)
    context = {
        "student_result": student_result,
    }
    return render(request, "student_template/student_view_result.html", context)
