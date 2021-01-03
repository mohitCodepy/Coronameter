from django.shortcuts import render

import requests
def country_call(request):
    country_list=[]
    url = "https://covid-193.p.rapidapi.com/statistics"
    headers = {
        'x-rapidapi-key': "b894b6f775mshb802c02ce55ee6cp19cd3ajsnff31519ced90",
        'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    r=response.json()
    number_of_countries = int(r['results'])
    for i in range(number_of_countries):
        country_list.append(r['response'][i]['country'])
    country_list = sorted(country_list)
    return country_list
def apicall(request, Country_name, country_list):
    Country_name = Country_name.capitalize()
    if Country_name =='':
        return
    elif Country_name not in country_list:
        Meme="kuchh to gadbad hai daya"
        print(Meme)
        return render(request,'Home.html',{'context':country_list, 'meme':Meme})
    url = "https://covid-193.p.rapidapi.com/statistics?country={}".format(Country_name)
    headers = {
        'x-rapidapi-key': "b894b6f775mshb802c02ce55ee6cp19cd3ajsnff31519ced90",
        'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers)
    r=response.json()    
    Cases={
        'Country' : r['response'][0]['country'],
        'New' : r['response'][0]['cases']['new'],
        'Active' : r['response'][0]['cases']['active'],
        'Recovered' : r['response'][0]['cases']['recovered'],
        'Total' : r['response'][0]['cases']['total'],
        }
    print("hello")
    return Cases
def home(request):
    country_list = country_call(request)
    if request.method=="POST":
        Country_name = request.POST.get('Country_name')
        Cases = apicall(request,Country_name,country_list)
        return render(request,'home.html',{'context':country_list, 'cases':Cases})
    return render(request,'home.html',{'context':country_list})
def search(request):
    if request.method == 'POST':
        Country_name = request.POST.get('covidsearch')
        country_list = country_call(request)
        Cases = apicall(request,Country_name,country_list)
        return render(request,'home.html', {'context':country_list, 'cases':Cases})
    else:
        country_list = country_call(request)
        return render(request,'home.html',{'context':country_list})
