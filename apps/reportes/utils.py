import csv
from django.http import HttpResponse


def export_as_csv(modeladmin, request, queryset, field_names, filename="export.csv"):
    """
    Exporta queryset a CSV con los campos indicados.
    field_names: lista de atributos del modelo (o propiedades)
    """
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset:
        row = []
        for field in field_names:
            value = getattr(obj, field)
            # si es callable (por ejemplo property), ejecutar
            if callable(value):
                value = value()
            row.append(value)
        writer.writerow(row)

    return response
