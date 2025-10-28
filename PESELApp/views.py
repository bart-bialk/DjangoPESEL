from django.shortcuts import render
from .forms import PeselForm

def validate_pesel(pesel):
    if not pesel.isdigit() or len(pesel) != 11:
        return {'valid': False, 'error': 'PESEL musi zawierać dokładnie 11 cyfr.'}

    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = sum(int(pesel[i]) * weights[i] for i in range(10))
    control_digit = (10 - (checksum % 10)) % 10

    if control_digit != int(pesel[-1]):
        return {'valid': False, 'error': 'Niepoprawna cyfra kontrolna PESEL.'}

    year = int(pesel[0:2])
    month = int(pesel[2:4])
    day = int(pesel[4:6])

    if 1 <= month <= 12:
        year += 1900
    elif 21 <= month <= 32:
        year += 2000
        month -= 20
    elif 41 <= month <= 52:
        year += 2100
        month -= 40
    elif 61 <= month <= 72:
        year += 2200
        month -= 60
    elif 81 <= month <= 92:
        year += 1800
        month -= 80
    else:
        return {'valid': False, 'error': 'Niepoprawny miesiąc w numerze PESEL.'}

    gender_digit = int(pesel[9])
    gender = "Kobieta" if gender_digit % 2 == 0 else "Mężczyzna"

    date_of_birth = f"{day:02d}-{month:02d}-{year}"

    return {
        'valid': True,
        'birth_date': date_of_birth,
        'gender': gender
    }


def pesel_view(request):
    result = None
    if request.method == 'POST':
        form = PeselForm(request.POST)
        if form.is_valid():
            pesel = form.cleaned_data['pesel']
            result = validate_pesel(pesel)
    else:
        form = PeselForm()

    return render(request, 'PESELApp/validator.html', {'form': form, 'result': result})

