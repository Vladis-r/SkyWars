from flask import Flask, render_template, request, redirect, url_for

from classes.base import Arena
from classes.classes import all_classes
from classes.equipment import Equipment
from classes.unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": PlayerUnit,
    "enemy": EnemyUnit
}

result_set_hero = {
    "header": "Выберите героя",  # для названия страниц
    "classes": all_classes.keys(),  # для названия классов
    "weapons": Equipment().get_weapons_names(),  # для названия оружия
    "armors": Equipment().get_armors_names()  # для названия брони
}

arena = Arena()


@app.route("/")
def menu_page():
    """
    Начальная страничка с 1 кнопкой
    """
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    """
    Страничка перед боем
    """
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes, result="Начнём битву")


@app.route("/fight/hit")
def hit():
    """
    Страничка после использования кнопки "Удар" во время боя
    """
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = "Игра окончена. Пойдём гулять!"
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    Страничка после использования кнопки "Использовать умение" во время боя
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = "Игра окончена. Пойдём гулять!"
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Страничка после использования кнопки "Пропуск хода" во время боя
    """
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = "Игра окончена. Пойдём гулять!"
    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    Страничка после использования кнопки "Конец игры" во время боя
    """
    arena.end_game()
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    """
    Страничка выбора героя для игрока
    """
    if request.method == "GET":
        return render_template("hero_choosing.html", result=result_set_hero)

    elif request.method == "POST":
        name = request.form["name"]
        set_class = request.form["unit_class"]
        weapon = request.form["weapon"]
        armor = request.form["armor"]

        new_player = PlayerUnit(name=name, unit_class=all_classes[set_class])
        new_player.equip_weapon(Equipment().get_weapon(weapon))
        new_player.equip_armor(Equipment().get_armor(armor))

        heroes["player"] = new_player
        return redirect(url_for("choose_enemy"), 200)


@app.route("/choose-enemy/", methods=['POST', 'GET'])
def choose_enemy():
    """
    Страничка выбора героя для компьютера
    """
    if request.method == "GET":
        return render_template("hero_choosing.html", result=result_set_hero)

    elif request.method == "POST":
        name = request.form["name"]
        set_class = request.form["unit_class"]
        weapon = request.form["weapon"]
        armor = request.form["armor"]

        enemy_player = EnemyUnit(name=name, unit_class=all_classes[set_class])
        enemy_player.equip_weapon(Equipment().get_weapon(weapon))
        enemy_player.equip_armor(Equipment().get_armor(armor))

        heroes["enemy"] = enemy_player
        return redirect(url_for("start_fight"), 200)


if __name__ == "__main__":
    app.run()
