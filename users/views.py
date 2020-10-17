from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now, localtime
import json, os
from .forms import UserRegisterForm
from .forms import ProfileForm
from .forms import WeightForm
from .forms import Lift2Form
from .forms import OptionForm
from .forms import FoodForm
from .models import Profile
from .models import WeightRecord
from .models import LiftRecord2
from .models import Food
import io, matplotlib, urllib, base64
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form' : form})

def login2(request, user):
    return render(request, 'users/login.html')

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        profForm = ProfileForm(request.POST, instance = profile)
        if profForm.is_valid():
            stillValid = True
            if profForm.cleaned_data['daily_cal_in'] < 0:
                messages.error(request, "Please enter a valid number of calories.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['daily_carbs'] < 0:
                messages.error(request, "Please enter a valid number of carbohydrates.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['daily_fat'] < 0:
                messages.error(request, "Please enter a valid number of fats.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['daily_protein'] < 0:
                messages.error(request, "Please enter a valid number of proteins.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['goal_weight_change'] < 0:
                messages.error(request, "Please enter a valid weight.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['starting_weight'] < 0:
                messages.error(request, "Please enter a valid weight.", extra_tags='danger')
                stillValid = False
            if profForm.cleaned_data['activity_level'] < 0:
                messages.error(request, "Please enter a valid activity level.", extra_tags='danger')
                stillValid = False
            if stillValid:
                profForm.save()
                messages.success(request, "Successfully updated profile!", extra_tags='success')
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = ProfileForm()
   
    #retrieve data in profile
    data = Profile.objects.filter(user = request.user)
    calories = carbs = fats = protein = goalWeight = currWeight = activity = starting_weight = {}
    for e in data:
        calories = e.daily_cal_in
        carbs = e.daily_carbs
        fats = e.daily_fat
        protein = e.daily_protein
        activity = e.activity_level
        startingWeight = e.starting_weight
        goalWeight = e.goal_weight_change

    #create graph for weight
    weightList = []
    dateList = []
    lbsList = []
    weights = WeightRecord.objects.filter(user=request.user).order_by('-date')
    for e in weights:
        weightList.append(e)
        lbsList.append(e.lbs)
        dateList.append(e.date)
    matplotlib.use('Agg')
    plt.plot(dateList, lbsList, marker='D', markersize=5)
    for i in range (0,len(lbsList)):
        plt.annotate(lbsList[i], (dateList[i], lbsList[i]), ha="center")
    plt.title('Weight Record')
    plt.xlabel('Date')
    plt.ylabel('Weight (lbs)')
    weightFig = plt.gcf()
    weightBuf = io.BytesIO()
    weightFig.savefig(weightBuf, format='png')
    weightBuf.seek(0)
    string = base64.b64encode(weightBuf.read())
    weightGraph = urllib.parse.quote(string)
    plt.close()

    #create graph for lifts
    exerciseNames = []
    exercises = LiftRecord2.objects.filter(user=request.user).order_by('-name')
    for e in exercises:
        if not e.name.lower().title() in exerciseNames:
           exerciseNames.append(e.name.lower().title())
    print(exerciseNames)
    chosenName = ""
    if request.method == 'POST' and 'option_submit' in request.POST:
        if request.POST.get('exercise', False):
            chosenName = request.POST['exercise']
    
    print(chosenName)

    chosenList = []
    date2List = []
    exercisesFiltered = LiftRecord2.objects.filter(user=request.user).order_by('-date')
    for e in exercisesFiltered:
        if e.name.lower().title() == chosenName:
            chosenList.append(e.weight)
            date2List.append(e.date)
    matplotlib.use('Agg')
    plt.plot(date2List, chosenList, marker='D', markersize=5)
    for i in range (0,len(chosenList)):
        plt.annotate(chosenList[i], (date2List[i], chosenList[i]), ha="center")
    plt.title(chosenName.title() + ' Record')
    plt.xlabel('Date')
    plt.ylabel('Weight (lbs)')
    strengthFig = plt.gcf()
    strengthBuf = io.BytesIO()
    strengthFig.savefig(strengthBuf, format='png')
    strengthBuf.seek(0)
    string = base64.b64encode(strengthBuf.read())
    strengthGraph = urllib.parse.quote(string)
    plt.close()

    #create pie chart for daily macros
    foodDates = []
    foods = Food.objects.filter(user=request.user).order_by('-date')
    for e in foods:
        if not e.date in foodDates:
           foodDates.append(e.date)
    print(foodDates)
    chosenDate = ""
    titleDate = ""
    if request.method == 'POST' and 'date_submit' in request.POST:
        if request.POST.get('date', False):
            chosenDate = request.POST['date']
            titleDate = chosenDate
            chosenDate = chosenDate.replace(".", "")
            chosenDate = datetime.datetime.strptime(str(parse(chosenDate)), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")

    percentages = [0,0,0]
    totalCal = 0
    macroLabels = 'Carbohydrates','Fats','Protein'
    fig3 = plt.figure(figsize =(10, 7)) 
    if chosenDate != "":
        foodsFiltered = Food.objects.filter(user=request.user,date=chosenDate)
        for e in foodsFiltered:
            print(chosenDate)
            print("matches")
            print(e.date)
            percentages[0] += e.carbs
            percentages[1] += e.fats
            percentages[2] += e.protein
            totalCal += e.calories
            print(e.calories)
        plt.pie(percentages, labels = macroLabels, autopct='%1.1f%%', shadow=True, startangle=90)
    totalCalStr = ""
    if titleDate != "":
        totalCalStr = "Total Calories: " + str(totalCal)
    plt.title("Macro Distribution " + str(titleDate) +"\n" + totalCalStr)
    macroFig = plt.gcf()
    macroBuf = io.BytesIO()
    macroFig.savefig(macroBuf, format='png')
    macroBuf.seek(0)
    string = base64.b64encode(macroBuf.read())
    macroGraph = urllib.parse.quote(string)
    matplotlib.use('Agg')
    plt.close()


    if len(weightList) != 0:
        currWeight = weightList[0].lbs
    context = {
        'loggedIn': False,
        'form': form,
        'calories' : calories,
        'carbs' : carbs,
        'fats' : fats,
        'protein' : protein,
        'activity' : activity,
        'startingWeight' : startingWeight,
        'goalWeight' : goalWeight,
        'currWeight' : currWeight,
        'weightGraph': weightGraph,
        'exerciseNames' : exerciseNames,
        'strengthGraph' : strengthGraph,
        'foodDates' : foodDates,
        'macroGraph' : macroGraph,
    }
    if request.user.is_authenticated:
        context['loggedIn'] = True
    return render(request, 'users/profile.html', context)

@login_required
def weight(request):
    weightrecord = WeightRecord(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        lbForm = WeightForm(request.POST, instance = weightrecord)
        if lbForm.is_valid():
            lbForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = WeightForm()
    data = WeightRecord.objects.filter(user = request.user).order_by('-date')
    context = {
        'form' : form,
        'weights' : data,
    }
    return render(request, 'users/weight.html', context)
  
@login_required
def macros(request):
    food = Food(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        foodForm = FoodForm(request.POST, instance = food)
        if foodForm.is_valid():
            foodForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = FoodForm()
    data = Food.objects.filter(user = request.user).order_by('-date')
    for e in data:
        carbCal = 4 * e.carbs
        fatCal = 9 * e.fats
        proteinCal = 4 * e.protein
        e.calories = carbCal + fatCal + proteinCal
        e.save()
    context = {
        'form' : form,
        'foods' : data,
    }

    return render(request, 'users/macros.html', context)
    
@login_required
def exercises(request):
    exercise_list = []

    with open(os.path.dirname(os.path.realpath(__file__)) + '/Exercises.json') as f:
        data = json.load(f)

    exercise_list = data

    liftrecord2 = LiftRecord2(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        liftForm = Lift2Form(request.POST, instance = liftrecord2)
        if liftForm.is_valid():
            liftForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = Lift2Form()
    data = LiftRecord2.objects.filter(user = request.user).order_by('-date')
    context = {
        'exercises': exercise_list,
        'title': 'Exercises',
        'form' : form,
        'lifts' : data,
    }

    return render(request, 'users/exercises.html', context)



@login_required
def meals(request):
    meal_dict = {}

    with open(os.path.dirname(os.path.realpath(__file__)) + '/Meals.json') as f:
        data = json.load(f)

    meal_dict = data

    # data = LiftRecord2.objects.filter(user = request.user).order_by('-date')
    context = {
        'meals': meal_dict,
        'title': 'Meals',
    }

    return render(request, 'users/meals.html', context)

