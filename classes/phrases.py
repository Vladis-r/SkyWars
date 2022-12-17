class Phrases:
    # armor_destroyed: str
    # armor_protects: str
    # not_enough_stamina: str
    # skill_use: str
    # no_stamina: str
    # skill_already_used: str

    def __init__(self):
        self.user_name = user_name
        self.weapon_name = weapon_name
        self.armor_name = armor_name
        self.skill_name = skill_name
        self.damage = damage

    def armor_destroy(self):
        return f"""
        {self.user_name}, используя {self.weapon_name}, 
        пробивает {self.armor_name} соперника и наносит {self.damage} урона."""

    def armor_protects(self):
        return f"""
        {self.user_name}, используя {self.weapon_name}, 
        наносит удар, но {self.armor_name} соперника его останавливает."""

    def not_enough_stamina(self):
        return f"""
        {self.user_name} попытался использовать {self.weapon_name}, 
        но у него не хватило выносливости."""

    def skill_use(self):
        return f"{self.user_name} использует {self.skill_name} и наносит {self.damage} урона сопернику."

    def no_stamina(self):
        return f"{self.user_name} попытался использовать {self.skill_name}, но у него не хватило выносливости."

    def skill_already_used(self):
        return "Навык уже использован."
