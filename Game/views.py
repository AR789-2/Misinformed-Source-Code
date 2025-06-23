from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import NameForm

rqt = None
Upgtag=""

Upgrades = {}
def Upgrade(name=str,results=dict,price=float, stages=1):
    global Upgrades
    for stage in range(stages):
        res2 = {}
        hint = ""
        for res in results:
            res2[res] = abs(results[res]) * 1+stage/3
            if results[res] < 0:
                res2[res] = 0-res2[res]
                hint += f"| {round(res2[res], 2)} {res} |"
            else:
                hint += f"| +{round(res2[res], 2)} {res} |"

        p = price*(stage+1)
        if stage == 0:
            p = price
        Upgrades[f"{name} {stage+1}"] = [res2, round(p), hint]
        if Upgtag != "All":
            try:
                if rqt.session[f"{name} {stage+1}"] == True:
                    continue
                else:
                    break
            except:
                rqt.session[f"{name} {stage+1}"] = False
                break
        else:
            rqt.session[f"{name} {stage+1}"] = False

def Upgrade_PriceIncrease(request):
    PI = 0
    PI += request.session["BEL"] * 2.75
    PI += request.session["SEV"] * 7
    PI *= request.session["ACT"] / 1.8
    PI /= 1.15
    for UPG in Upgrades:
        Upgrades[UPG][1] += round(PI)

def UpgradeListAll(request,tag=""):
    global Upgrades
    Upgrades = {}
    global Upgtag
    Upgtag = tag
    global rqt
    rqt = request
    #Get All Upgrades
    Upgrade("First Lie", {
        "ACT": 1
    }, 0, 1)
    if rqt.session["First Lie 1"]:
        Upgrade("Social Media", {
            "ACT": 0.5,
            "SEV": 0.15,
            "BEL": 0.2,
        }, 10, 5)
        Upgrade("Word of Mouth", {
            "ACT": 0.25,
            "SEV": 0.1,
            "BEL": 0.35,
        }, 15, 4)
        Upgrade("Deception", {
            "ACT": 0.1,
            "SEV": 0.2,
            "BEL": 0.37,
        }, 22, 3)
        Upgrade("Propoganda", {
            "ACT": 0.6,
            "SEV": 0.35,
            "BEL": 0.15,
        }, 18, 4)
        Upgrade("Memes", {
            "ACT": 0.85,
            "SEV": 0.1,
            "BEL": 0.1,
        }, 12, 4)
        Upgrade("Fact Check", {
            "ACT": 0,
            "SEV": -0.35,
            "BEL": 0.02,
        }, 16, 5)
        Upgrade("Advertise", {
            "ACT": 0.05,
            "SEV": 0.03,
            "BEL": 0.036,
        }, 5, 999)

    return Upgrades

def purchase(request, upg_id):
    UpgradeList = UpgradeListAll(request) #Gets all avaliable Upgrades
    Upgrade_PriceIncrease(request)
    if request.session["Cash"] >= UpgradeList[upg_id][1] and not request.session[upg_id]:
        request.session["Cash"] -= UpgradeList[upg_id][1]
        for stat in UpgradeList[upg_id][0]:
            request.session[stat] += UpgradeList[upg_id][0][stat]
        request.session[upg_id] = True
    return redirect('Game:upgrade')


# Create your views here.
def index(request):
    se = round(request.session["SEV"],2)
    if se < 0:
        se = 0

    return render(request, "game/index.html", {
            'PartyName': request.session["PartyName"],
                'Cash': request.session["Cash"],
                "ACT": round(request.session["ACT"],2),
                "BEL": round(request.session["BEL"],2),
                "SEV": se,
                "REP": request.session["REPUTATION"],
        })

def SETREPUTATION(request, rep, profit):
    request.session["REPUTATION"] = rep
    request.session["Cash"] = request.session["Cash"] + profit
    return redirect('Game:upgrade')

def upgrade(request):
    UpgradeList = UpgradeListAll(request) #Gets all avaliable Upgrades
    Upgrade_PriceIncrease(request)
    for u in UpgradeList:
        try:
            if request.session[u] == True:
                UpgradeList[u] = "BOUGHT"
        except:
            None

    se = round(request.session["SEV"],2)
    if se < 0:
        se = 0

    return render(request, "game/upgrade.html", {
        'Cash': request.session["Cash"],
        "ACT": round(request.session["ACT"],2),
        "BEL": round(request.session["BEL"],2),
        "SEV": se,
        "Upgrades": UpgradeList
    })

def name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            request.session["Cash"] = 0
            request.session["ACT"] = 0
            request.session["BEL"] = 0
            request.session["SEV"] = 0
            request.session["REPUTATION"] = 0
            request.session["PartyName"] = form.data['your_name']
            UpgradeList = UpgradeListAll(request, "ALL")
            for u in UpgradeList:
                request.session[u] = False
            return redirect("Game:index")
    else:
        form = NameForm()
    
    return render(request, "game/name.html")

def win(request):
    return render(request, "game/win.html", {
        "Lie": request.session["PartyName"]
    })

def loss(request):
    return render(request, "game/loss.html", {
        "Lie": request.session["PartyName"]
    })