from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now, localtime
import json, os
from .forms import *
from .models import *
import io, matplotlib, urllib, base64
import re
import matplotlib.pyplot as plt
import datetime
from dateutil.parser import parse
import requests 
from bs4 import BeautifulSoup
import cchardet as chardet
import lxml
import concurrent.futures


URLS = [
    {'Abs' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/abs/'},
    {'Biceps' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/arms/biceps/'},
    {'Butt/Hip' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/butt-hips/'},
    {'Calves' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/legs-calves-and-shins/soleus/'},
    {'Chest' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/chest/'},
    {'Lats' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/back/latissimus-dorsi(lats)/'},
    {'Shoulders' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/shoulders/'},
    {'Trapezius' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/back/trapezius(traps)/'},
    {'Triceps' : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/arms/triceps/'},
    {'Quads'  : 'https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/legs-calves-and-shins/soleus/'}
]

EXERCISES_GLOBAL = []


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
    if request.method == 'POST' and 'form_submit' in request.POST:
        update_prof_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if update_prof_form.is_valid():
            update_prof_form.save()
            messages.success(request, "Successfully updated profile data!", extra_tags='success')
            return redirect('profile')
        else:
            messages.error(request, "Please check entries are valid", extra_tags='danger')
    else:
        update_prof_form = ProfileUpdateForm(instance=request.user.profile)


    #retrieve data in profile
    data = Profile.objects.filter(user = request.user)
    calories = carbs = fats = protein = goalWeight = currWeight = activity = starting_weight = {}
    for e in data:
        calories = e.daily_cal_in
        carbs = e.daily_carbs
        fats = e.daily_fat
        protein = e.daily_protein
        activity = e.activity_level
        weight = e.weight
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
    plt.style.use('ggplot')
    plt.plot(dateList, lbsList, marker='D', markersize=5)
    for i in range(0, len(lbsList)):
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
    chosenName = ""
    if request.method == 'POST' and 'option_submit' in request.POST:
        if request.POST.get('exercise', False):
            chosenName = request.POST['exercise']
    

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

    daily_activity_desc = ["""Very light - Seated and standing activities, office work, driving, cooking; 
                           no vigorous activity
                           """,
                           """
                           Low active - In addition to the activities of a sedentary lifestyle, 30 minutes of moderate 
                           activity equivalent of walking 2 mines in 30 minutes; most office workers with additional planned exercis routines
                           """,
                           """
                           Active - In addition to the activities of a low active lifestyle, an additional 3 hours of 
                           activity such as bicycle 10-12 miles an hour, walk 4.5 miles an hour
                           """,
                           """
                           Heavy - Planned vigorous activities, physical labor, full-time athletes, hard-labor 
                           professions such as steel or road workers
                           """]
    if Profile.objects.filter(user=request.user).first().activity_level<1.4:
        daily_act = daily_activity_desc[0]
    elif Profile.objects.filter(user=request.user).first().activity_level<1.7:
        daily_act = daily_activity_desc[1]
    elif Profile.objects.filter(user=request.user).first().activity_level<1.8:
        daily_act = daily_activity_desc[2]
    else:
        daily_act = daily_activity_desc[3]
    if len(weightList) != 0:
        currWeight = weightList[0].lbs
    context = {
        'username': request.user.username,
        'loggedIn': False,
        'daily_act_info':daily_act,
        'update_prof_form': update_prof_form,
        'calories' : calories,
        'carbs' : carbs,
        'fats' : fats,
        'protein' : protein,
        'activity' : activity,
        'weight' : weight,
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
    foodName = ""
    foodDate = ""
    display = False
    if request.method == 'POST' and 'form2_submit' in request.POST:
        display = True
        singleFood = SingleFood(request.POST)
        if singleFood.is_valid():
            foodName = singleFood.cleaned_data['foodName'].capitalize()
            foodDate = singleFood.cleaned_data['date']
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')        

        # URL = "https://www.acefitness.org/education-and-resources/lifestyle/exercise-library/body-part/abs/"
        r = requests.get("https://www.myfitnesspal.com/food/search?page=1&search="+str(foodName)) 

        soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
        if soup.find('div', attrs = {"class": "jss16"}) == None:
            print("rip")
        else:
            macroData = soup.find('div', attrs = {"class": "jss16"}).text
            servingSize = soup.find('div', attrs = {"class": "jss11"}).text
            servingSize = servingSize[servingSize.find(",")+2:]
            macroList = re.findall(r'[0-9]+', macroData) 
            print(macroData)
            print(macroList)
            print(servingSize)
            print("Calories: " + str(macroList[0]))
            print("Carbs: " + str(macroList[1]))
            print("Fat: " + str(macroList[2]))
            print("Protein: " + str(macroList[3]))
            food2 = Food(user=request.user)
            food2.name = foodName
            food2.calories = macroList[0]
            food2.carbs = macroList[1]
            food2.fats = macroList[2]
            food2.protein = macroList[3]
            food2.date = foodDate
            food2.save()
    form2 = SingleFood()
           
            
    food = Food(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        foodForm = FoodForm(request.POST, instance = food)
        if foodForm.is_valid():
            food.name = foodForm.cleaned_data['name'].capitalize()
            foodForm.save()
            return redirect('macros')
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
        'form2': form2,
        'foods' : data,
        'display' : display,
    }

    return render(request, 'users/macros.html', context)
    
@login_required
def exercises(request):
    lift_form_name = ""

    category = 'All'
    if request.method == 'POST':

        filter_form = ExerciseFilterForm(request.POST)
        if filter_form.is_valid():
            category = filter_form.cleaned_data['category']
            print(category)
        else:
            lift_form_name = request.POST['form_submit']
            print(request.POST['form_submit'])
    # EXERCISES_GLOBAL = []
    if category == 'All':
        threads = len(URLS)
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(scrap_url, URLS)

    else:
        EXERCISES_GLOBAL.clear()
        correct_index = 0
        for index, url in enumerate(URLS):
            for key in url:
                if key == category:
                    correct_index = index

        r = requests.get(URLS[correct_index][category])
        soup = BeautifulSoup(r.content,
                             'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
        table = soup.find('div', attrs={'id': 'exerciseLibrary'})
        for row in table.findAll('div', attrs={"class": "exercise-card-grid__cell"}):
            exercise = {}
            exercise['category'] = category
            # exercise = {}
            exercise['name'] = row.find('div', attrs={"class": "exercise-card__body"}).header.h2.text
            # exercise['name'] = row.header.h2.text

            exercise['equipment'] = row.find('div', attrs={
                "class": "exercise-info__term exercise-info__term--equipment"}).dd.text
            exercise['img'] = row.find('div', attrs={"class": "exercise-card__image"})['style'].split("'")[1]
            exercise['description_link'] = 'https://www.acefitness.org/' + row.a['href']

            EXERCISES_GLOBAL.append(exercise)

    filter_form = ExerciseFilterForm(initial={'category': category})

    liftrecord2 = LiftRecord2(user=request.user)
    if request.method == 'POST' and 'form_submit' in request.POST:
        liftForm = Lift2Form(request.POST, instance=liftrecord2)
        if liftForm.is_valid():
            liftForm.save()
        else:
            messages.error(request, "Please re-enter valid information.", extra_tags='danger')
    form = Lift2Form(initial={'name': lift_form_name})
    # filter_form = ExerciseFilterForm()
    data = LiftRecord2.objects.filter(user=request.user).order_by('-date')
    print(EXERCISES_GLOBAL)
    context = {
        'exercises': EXERCISES_GLOBAL,
        'title': 'Exercises',
        'form': form,
        'filter': filter_form,
        'lifts': data,
    }

    return render(request, 'users/exercises.html', context)


def scrap_url(url):
    for key in url:
        r = requests.get(url[key])

        soup = BeautifulSoup(r.content,
                             'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib

        table = soup.find('div', attrs={'id': 'exerciseLibrary'})
        print("OVER THERE")
        for row in table.findAll('div', attrs={"class": "exercise-card-grid__cell"}):
            print("Over here")
            exercise = {}
            exercise['category'] = key
            # exercise = {}
            exercise['name'] = row.find('div', attrs={"class": "exercise-card__body"}).header.h2.text
            # exercise['name'] = row.header.h2.text

            exercise['equipment'] = row.find('div', attrs={
                "class": "exercise-info__term exercise-info__term--equipment"}).dd.text
            exercise['img'] = row.find('div', attrs={"class": "exercise-card__image"})['style'].split("'")[1]
            exercise['description_link'] = 'https://www.acefitness.org/' + row.a['href']
            EXERCISES_GLOBAL.append(exercise)

@login_required
def meals(request):

    category = 'All'
    if request.method == 'POST':
        filter_form = MealFilterForm(request.POST)
        if filter_form.is_valid():
            category = filter_form.cleaned_data['category']

    if category != 'All':
        URL = 'https://www.skinnytaste.com/recipes/' + category + '/'
    else:
        URL = 'https://www.skinnytaste.com/recipes/'

    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'lxml')
    recipe_list = []
    recipe_dict = {}

    for tag in soup.find_all('div', class_="archive-post"):
        recipe_dict['link'] = tag.find('a')['href']
        recipe_dict['title'] = tag.find('a')['title']
        recipe_dict['img'] = tag.find('img')['src']
        recipe_list.append(recipe_dict)
        recipe_dict = {}

    count = 1
    while count < 5:
        URL = 'https://www.skinnytaste.com/recipes/page/' + str(count) + '/'
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'lxml')
        count += 1
        for tag in soup.find_all('div', class_="archive-post"):
            recipe_dict['link'] = tag.find('a')['href']
            recipe_dict['title'] = tag.find('a')['title']
            recipe_dict['img'] = tag.find('img')['src']
            recipe_list.append(recipe_dict)
            recipe_dict = {}

    filter_form = MealFilterForm(initial={'category': category})
    context = {
        'meals': recipe_list,
        'title': 'Meals',
        'filter': filter_form,
    }

    return render(request, 'users/meals.html', context)