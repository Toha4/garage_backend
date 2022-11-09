from ..models import Material


def update_car_tag_material(old_name: str, new_name: str):
    materials = Material.objects.filter(compatbility__contains=[old_name])
    for material in materials:
        material.compatbility = [new_name if car_tag == old_name else car_tag for car_tag in material.compatbility]
        material.save()
