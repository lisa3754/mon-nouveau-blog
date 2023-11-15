from django.shortcuts import render, get_object_or_404, redirect
from .models import Equipement, Character
from .forms import MoveForm
from django.contrib import messages

def post_list(request):
    characters = Character.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/post_list.html', {'characters': characters, 'equipements': equipements})

def post_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    lieu = character.lieu
    form=MoveForm()
    if request.method == "POST":
        ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        form = MoveForm(request.POST, instance=character)
        if form.is_valid():
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            if nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Paddock" and character.etat=='Affamé':
                character.etat="Repus"
                character.save()
                nouveau_lieu.disponibilite="Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre cheval a bien été emmenené au paddock !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Carrière" and character.etat=='Repus':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                character.etat="Fatigué"
                character.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre cheval est entraîné dans la carrière !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Box" and character.etat=='Fatigué':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                character.etat="Endormi"
                character.save()
                nouveau_lieu.disponibilite = "Occupé"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre cheval est bien dans son box !')
            elif nouveau_lieu.disponibilite=="Libre" and nouveau_lieu.id_equip=="Pré" and character.etat=='Endormi':
                ancien_lieu.disponibilite="Libre"
                ancien_lieu.save()
                character.etat="Affamé"
                character.save()
                nouveau_lieu.disponibilite = "Libre"
                nouveau_lieu.save()
                messages.add_message(request, messages.SUCCESS, 'Votre cheval a bien été emmenené au pré !')
            elif nouveau_lieu==ancien_lieu:
                messages.add_message(request, messages.WARNING, 'Votre cheval est déjà à cet endroit.')
            else :
                print('message')
                messages.add_message(request, messages.ERROR, 'Désolé, vous ne pouvez pas emmenez ce cheval à cet endroit.')
        return redirect('post_detail', id_character=id_character)
    else:
        form = MoveForm()
        return render(request,
                  'blog/post_detail.html',
                  {'character': character, 'lieu': lieu, 'form': form})