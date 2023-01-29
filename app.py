from typing import Union, Type, Any, Optional

from base import Arena
from classes import unit_classes
from equipment import Equipment
from flask import Flask, render_template, request, redirect, url_for
from unit import BaseUnit, PlayerUnit, EnemyUnit


app = Flask(__name__)

heroes = {
    "player": Optional[BaseUnit],
    "enemy": Optional[BaseUnit]
}

arena = Arena()


@app.route("/")
def menu_page() -> str:
    # TODO рендерим главное меню (шаблон index.html)
    return render_template("index.html")


@app.route("/fight/")
def start_fight() -> str:
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit() -> str:
    if arena.game_is_running:
        res = arena.player_hit()
    else:
        res = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=res)


@app.route("/fight/use-skill")
def use_skill() -> str:
    if arena.game_is_running:
        res = arena.player_use_skill()
    else:
        res = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=res)


@app.route("/fight/pass-turn")
def pass_turn() -> str:
    if arena.game_is_running:
        res = arena.next_turn()
    else:
        res = arena.battle_result
    return render_template("fight.html", heroes=heroes, result=res)


@app.route("/fight/end-fight")
def end_fight() -> str:
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero() -> str | Any:
    if request.method == "GET":
        equipment: Equipment = Equipment()
        res = {
            "header": "Choose hero",  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()
        }
        return render_template("hero_choosing.html", result=res)
    if request.method == "POST":
        name = request.form["name"]
        weapon = request.form["weapon"]
        armor = request.form["armor"]
        unit_class = request.form["unit_class"]

        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        player.equip_weapon(Equipment().get_weapon(weapon_name=weapon))
        player.equip_armor(Equipment().get_armor(armor_name=armor))
        heroes["player"] = player
        return redirect(url_for("choose_enemy"))
    return ""


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy() -> str | Any:
    if request.method == "GET":
        equipment = Equipment()
        res = {
            "header": "Choose hero",  # для названия страниц
            "classes": unit_classes,  # для названия классов
            "weapons": equipment.get_weapons_names(),  # для названия оружия
            "armors": equipment.get_armors_names()
        }
        return render_template("hero_choosing.html", result=res)
    if request.method == "POST":
        name = request.form["name"]
        weapon = request.form["weapon"]
        armor = request.form["armor"]
        unit_class = request.form["unit_class"]

        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        enemy.equip_weapon(Equipment().get_weapon(weapon_name=weapon))
        enemy.equip_armor(Equipment().get_armor(armor_name=armor))
        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))
    return ""

if __name__ == "__main__":
    app.run()
