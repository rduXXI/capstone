from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib import colors
from orden_pedido.models import OrdenPedido
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter
import tempfile
from num2words import num2words
from django.shortcuts import get_object_or_404


@staff_member_required
def lista_ordenes_pedido(request):
    ordenes = OrdenPedido.objects.all().order_by("-fecha_creacion")
    return render(request, "components/lista_ordenes_pedido.html", {"ordenes": ordenes})


@staff_member_required
def detalle_orden_pedido(request, orden_id):
    orden = get_object_or_404(OrdenPedido, id=orden_id)
    productos_canjeados = orden.productos_canjeados.all()

    return render(
        request,
        "components/detalle_orden_pedido.html",
        {"orden": orden, "productos_canjeados": productos_canjeados},
    )


def generar_factura_pdf(request, orden_id):
    # Obtener la orden de pedido y productos

    orden = get_object_or_404(OrdenPedido, id=orden_id)
    productos_canjeados = orden.productos_canjeados.all()

    # Configurar respuesta PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="factura_orden_{orden_id}.pdf"'
    )

    # Crear PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    ancho_pagina, alto_pagina = A4
    x, y = 50, alto_pagina - 200  # Posiciones iniciales para el cuadro

    # Tabla de documentos de referencia
    fecha_emision = [
        ["FECHA DE EMISIÓN", f"{orden.fecha_creacion.strftime('%d/%m/%Y')}"],
    ]

    y_pos_fecha_emision = alto_pagina - 40
    table_fecha_emision = Table(fecha_emision)
    table_fecha_emision.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
            ]
        )
    )
    table_fecha_emision.wrapOn(p, ancho_pagina, alto_pagina)
    table_fecha_emision.drawOn(p, 235, y_pos_fecha_emision)

    factura = [
        ["R.U.T: 12.345.678-9"],
        ["FACTURA ELECTRÓNICA"],
    ]
    y_pos_factura = alto_pagina - 40
    table_factura = Table(factura)
    table_factura.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("BACKGROUND", (0, 0), (0, -1), colors.white),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
            ]
        )
    )
    table_factura.wrapOn(p, ancho_pagina, alto_pagina)
    table_factura.drawOn(p, 440, y_pos_factura)

    # Dibujar cuadro de información
    p.setStrokeColorRGB(0, 0, 0)
    p.setLineWidth(0.5)
    p.rect(x, y, 500, 150)
    p.setFont("Helvetica-Bold", 8)
    p.drawString(x + 10, y + 130, "RAZÓN SOCIAL:")
    p.drawString(
        x + 75, y + 130, f"{orden.empleado.first_name} {orden.empleado.last_name}"
    )
    p.drawString(x + 10, y + 110, "RUN:")
    p.drawString(x + 75, y + 110, f"{orden.razon_social.run}-{orden.razon_social.dv}")
    p.drawString(x + 10, y + 90, "GIRO: COMERCIAL")
    p.drawString(x + 10, y + 70, "DIRECCIÓN COMERCIAL:")
    p.drawString(
        x + 20, y + 60, f"{orden.empleado.first_name} {orden.empleado.last_name}"
    )
    p.drawString(x + 20, y + 50, str(orden.razon_social.direccion))
    p.drawString(
        x + 210, y + 130, f"FECHA DE PAGO: {orden.fecha_creacion.strftime('%d/%m/%Y')}"
    )
    p.drawString(x + 210, y + 110, "MONEDA: MONEDA NACIONAL")
    p.drawString(x + 210, y + 90, f"ORDEN DE COMPRA: {orden.empleado}")

    # Tabla de documentos de referencia
    refs_docs = [
        [
            "ID doc.",
            "Tipo Documento",
            "Folio",
            "Fecha de Documento",
            "Razón Referencia",
            "Cod. Referencia",
        ]
    ]
    refs_docs.append(
        [
            str(orden.id),
            "Orden de compra",
            f"{orden.empleado}",
            orden.fecha_creacion.strftime("%d/%m/%Y"),
            "",
            "",
        ]
    )
    y_pos_refs_docs = alto_pagina - 250
    table_refs_docs = Table(refs_docs, colWidths=[50, 100, 45, 100, 105, 100])
    table_refs_docs.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table_refs_docs.wrapOn(p, ancho_pagina, alto_pagina)
    table_refs_docs.drawOn(p, x, y_pos_refs_docs)

    # Tabla de productos
    data_productos = [
        [
            "N°",
            "Cantidad",
            "Código",
            "Producto",
            "Pts. Unit",
            "Pcio. Unit",
            "Descripción",
            "Grado alcohólico",
        ]
    ]
    for i, producto in enumerate(productos_canjeados, start=1):
        data_productos.append(
            [
                str(i),
                str(producto.cantidad),
                str(producto.producto.id),
                f"{producto.producto.nombre} {producto.producto.contenido} ml",
                f"{producto.producto.puntos_requeridos}",
                f"{producto.producto.precio_unitario}",
                producto.producto.descripcion,
                f"{producto.producto.abv}%",
            ]
        )
    y_pos_productos = alto_pagina - 300
    table_productos = Table(data_productos, colWidths=[20, 45, 45, 140, 50, 50, 70, 80])
    table_productos.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table_productos.wrapOn(p, ancho_pagina, alto_pagina)
    table_productos.drawOn(p, x, y_pos_productos)
    monto_neto = sum(
        producto.producto.precio_unitario * producto.cantidad
        for producto in productos_canjeados
    )
    iva = monto_neto * 0.19
    monto_total = monto_neto + iva
    data_totales = [
        ["DESCUENTOS", "0"],
        ["MONTO EXENTO", "0"],
        ["MONTO NETO", f"{round(monto_neto)}"],
        ["19% IVA", f"{round(iva)}"],
        ["MONTO TOTAL", f"{round(monto_total)}"],
    ]
    y_pos_totales = alto_pagina - 600
    table_totales = Table(data_totales, colWidths=[100, 100])
    table_totales.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
            ]
        )
    )
    table_totales.wrapOn(p, ancho_pagina, alto_pagina)
    table_totales.drawOn(p, 350, y_pos_totales)

    barcode_data = str(monto_total)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        Code128(barcode_data, writer=ImageWriter()).write(tmp_file)
        p.drawImage(tmp_file.name, x + 10, 40, width=250, height=150)

    monto_total_palabras = num2words(
        monto_total, to="currency", lang="es", currency="CLP"
    ).replace("dólares", "pesos")

    p.setFont("Helvetica", 6)

    p.drawString(x + 80, 190, monto_total_palabras)

    p.showPage()

    p.save()

    buffer.seek(0)

    response.write(buffer.read())

    return response


@login_required
def enviar_factura_email(request, orden_id):
    # Obtener la orden de pedido y productos

    orden = get_object_or_404(OrdenPedido, id=orden_id)
    productos_canjeados = orden.productos_canjeados.all()

    # Configurar respuesta PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="factura_orden_{orden_id}.pdf"'
    )

    # Crear PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    ancho_pagina, alto_pagina = A4
    x, y = 50, alto_pagina - 200  # Posiciones iniciales para el cuadro

    # Tabla de documentos de referencia
    fecha_emision = [
        ["FECHA DE EMISIÓN", f"{orden.fecha_creacion.strftime('%d/%m/%Y')}"],
    ]

    y_pos_fecha_emision = alto_pagina - 40
    table_fecha_emision = Table(fecha_emision)
    table_fecha_emision.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
            ]
        )
    )
    table_fecha_emision.wrapOn(p, ancho_pagina, alto_pagina)
    table_fecha_emision.drawOn(p, 235, y_pos_fecha_emision)

    factura = [
        ["R.U.T: 12.345.678-9"],
        ["FACTURA ELECTRÓNICA"],
    ]
    y_pos_factura = alto_pagina - 40
    table_factura = Table(factura)
    table_factura.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("BACKGROUND", (0, 0), (0, -1), colors.white),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.black),
            ]
        )
    )
    table_factura.wrapOn(p, ancho_pagina, alto_pagina)
    table_factura.drawOn(p, 440, y_pos_factura)

    # Dibujar cuadro de información
    p.setStrokeColorRGB(0, 0, 0)
    p.setLineWidth(0.5)
    p.rect(x, y, 500, 150)
    p.setFont("Helvetica-Bold", 8)
    p.drawString(x + 10, y + 130, "RAZÓN SOCIAL:")
    p.drawString(
        x + 75, y + 130, f"{orden.empleado.first_name} {orden.empleado.last_name}"
    )
    p.drawString(x + 10, y + 110, "RUN:")
    p.drawString(x + 75, y + 110, f"{orden.razon_social.run}-{orden.razon_social.dv}")
    p.drawString(x + 10, y + 90, "GIRO: COMERCIAL")
    p.drawString(x + 10, y + 70, "DIRECCIÓN COMERCIAL:")
    p.drawString(
        x + 20, y + 60, f"{orden.empleado.first_name} {orden.empleado.last_name}"
    )
    p.drawString(x + 20, y + 50, str(orden.razon_social.direccion))
    p.drawString(
        x + 210, y + 130, f"FECHA DE PAGO: {orden.fecha_creacion.strftime('%d/%m/%Y')}"
    )
    p.drawString(x + 210, y + 110, "MONEDA: MONEDA NACIONAL")
    p.drawString(x + 210, y + 90, f"ORDEN DE COMPRA: {orden.empleado}")

    # Tabla de documentos de referencia
    refs_docs = [
        [
            "ID doc.",
            "Tipo Documento",
            "Folio",
            "Fecha de Documento",
            "Razón Referencia",
            "Cod. Referencia",
        ]
    ]
    refs_docs.append(
        [
            str(orden.id),
            "Orden de compra",
            f"{orden.empleado}",
            orden.fecha_creacion.strftime("%d/%m/%Y"),
            "",
            "",
        ]
    )
    y_pos_refs_docs = alto_pagina - 250
    table_refs_docs = Table(refs_docs, colWidths=[50, 100, 45, 100, 105, 100])
    table_refs_docs.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table_refs_docs.wrapOn(p, ancho_pagina, alto_pagina)
    table_refs_docs.drawOn(p, x, y_pos_refs_docs)

    # Tabla de productos
    data_productos = [
        [
            "N°",
            "Cantidad",
            "Código",
            "Producto",
            "Pts. Unit",
            "Pcio. Unit",
            "Descripción",
            "Grado alcohólico",
        ]
    ]
    for i, producto in enumerate(productos_canjeados, start=1):
        data_productos.append(
            [
                str(i),
                str(producto.cantidad),
                str(producto.producto.id),
                f"{producto.producto.nombre} {producto.producto.contenido} ml",
                f"{producto.producto.puntos_requeridos}",
                f"{producto.producto.precio_unitario}",
                producto.producto.descripcion,
                f"{producto.producto.abv}%",
            ]
        )
    y_pos_productos = alto_pagina - 300
    table_productos = Table(data_productos, colWidths=[20, 45, 45, 140, 50, 50, 70, 80])
    table_productos.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table_productos.wrapOn(p, ancho_pagina, alto_pagina)
    table_productos.drawOn(p, x, y_pos_productos)
    monto_neto = sum(
        producto.producto.precio_unitario * producto.cantidad
        for producto in productos_canjeados
    )
    iva = monto_neto * 0.19
    monto_total = monto_neto + iva
    data_totales = [
        ["DESCUENTOS", "0"],
        ["MONTO EXENTO", "0"],
        ["MONTO NETO", f"{round(monto_neto)}"],
        ["19% IVA", f"{round(iva)}"],
        ["MONTO TOTAL", f"{round(monto_total)}"],
    ]
    y_pos_totales = alto_pagina - 600
    table_totales = Table(data_totales, colWidths=[100, 100])
    table_totales.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("BACKGROUND", (0, 0), (0, -1), colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.whitesmoke),
            ]
        )
    )
    table_totales.wrapOn(p, ancho_pagina, alto_pagina)
    table_totales.drawOn(p, 350, y_pos_totales)

    barcode_data = str(monto_total)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        Code128(barcode_data, writer=ImageWriter()).write(tmp_file)
        p.drawImage(tmp_file.name, x + 10, 40, width=250, height=150)

    monto_total_palabras = num2words(
        monto_total, to="currency", lang="es", currency="CLP"
    ).replace("dólares", "pesos")

    p.setFont("Helvetica", 6)

    p.drawString(x + 80, 190, monto_total_palabras)

    p.showPage()

    p.save()

    buffer.seek(0)

    response.write(buffer.read())

    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    # Crear y enviar el correo
    email = EmailMessage(
        subject=f"Factura de Pedido #{orden.id}",
        body=f"Estimado {orden.empleado.first_name} {orden.empleado.last_name}, adjunto encontrarás la factura correspondiente a tu pedido #{orden.id}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[orden.empleado.email],
    )

    # Adjuntar el PDF al correo
    email.attach(f"factura_orden_{orden.id}.pdf", pdf, "application/pdf")
    email.send()

    messages.success(request, "La factura ha sido enviada al correo del empleado.")
    return redirect("facturas")


def lista_facturas(request):
    # Obtener todas las órdenes en estado aprobadas
    ordenes_pendientes = OrdenPedido.objects.filter(estado="Aprobada").order_by(
        "-fecha_creacion"
    )

    return render(request, "components/facturas.html", {"ordenes": ordenes_pendientes})
