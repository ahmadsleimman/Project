from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Class, ClassRequest, ClassMessage, ClassFinancialAid
from Main.models import Student, Teacher


# Create your views here.

def Classes(request):
    classes = Class.objects.all()

    context = {
        "classes": classes,
    }

    return render(request, 'classes/classes.html', context)


@login_required(login_url='Login')
def ClassDetails(request, id):
    try:
        myclass = Class.objects.get(id=id)
    except:
        return redirect("NotFound")

    classmessages = ClassMessage.objects.filter(myclass=myclass)

    context = {
        "class": myclass,
        "classmessages": classmessages,
    }

    if hasattr(request.user, 'student'):
        isEnrolled = None
        isFinancial = None

        student = Student.objects.get(user=request.user)

        if student in myclass.students.all():
            isEnrolled = True

        try:
            classrequest = ClassRequest.objects.get(student=student, myclass=myclass)
            isRequested = True
        except:
            isRequested = False

        try:
            classfinancial = ClassFinancialAid.objects.get(student=student, myclass=myclass)
            isFinancial = True
        except:
            isFinancial = False

        context.update({"isEnrolled": isEnrolled})
        context.update({"isRequested": isRequested})
        context.update({"isFinancial": isFinancial})

    if hasattr(request.user, 'teacher'):
        isAdmin = None
        teacher = Teacher.objects.get(user=request.user)

        if teacher == myclass.teacher:
            isAdmin = True

        context.update({"isAdmin": isAdmin})

    return render(request, 'classes/class-details.html', context)


@login_required(login_url='Login')
def ClassEnroll(request, id):
    try:
        myclass = Class.objects.get(id=id)
    except:
        return redirect("NotFound")

    if hasattr(request.user, 'student'):
        studentID = Student.objects.get(user=request.user)
        classrequest = ClassRequest.objects.create(student=studentID, myclass=myclass)
    return redirect("ClassDetails", id=id)


@login_required(login_url='Login')
def ClassFinancialAidEnroll(request, id):
    try:
        myclass = Class.objects.get(id=id)
    except:
        return redirect("NotFound")

    context = {
        "class": myclass
    }

    if request.method == "POST" and hasattr(request.user, 'student'):
        studentID = Student.objects.get(user=request.user)
        message = request.POST['message']
        ClassFinancialAid.objects.create(student=studentID, myclass=myclass, message=message)
        return redirect("ClassDetails", id=id)

    return render(request, 'classes/class-financialaid.html', context)
