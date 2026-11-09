import json
from io import BytesIO
from django.http import HttpResponse
from django.utils.html import escape
from docx import Document
from weasyprint import HTML

def clean(data):
    return data if isinstance(data, dict) else {}

def export_json(cv):
    payload = {"title": cv.title, "language": cv.language, "template": cv.template, "data": cv.data}
    response = HttpResponse(json.dumps(payload, ensure_ascii=False, indent=2), content_type="application/json; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{cv.title.replace(" ", "_")}.json"'
    return response

def sections_html(cv):
    d = clean(cv.data); p = d.get("personal", {})
    name = escape(p.get("name", "")); headline = escape(p.get("headline", ""))
    contact = " · ".join(escape(str(p.get(k, ""))) for k in ("email", "phone", "location", "website") if p.get(k))
    sections = []
    def add_section(title, rows):
        if not rows: return
        body = ""
        for item in rows:
            if isinstance(item, str):
                body += f"<li>{escape(item)}</li>"
            else:
                heading = escape(str(item.get("role") or item.get("degree") or item.get("name") or item.get("title") or ""))
                sub = escape(str(item.get("company") or item.get("institution") or item.get("issuer") or item.get("organization") or ""))
                dates = escape(str(item.get("dates") or ""))
                desc = escape(str(item.get("description") or item.get("details") or ""))
                body += f"<div class='entry'><b>{heading}</b><span>{sub} {dates}</span><p>{desc}</p></div>"
        sections.append(f"<section><h2>{escape(title)}</h2>{'<ul>'+body+'</ul>' if all(isinstance(x,str) for x in rows) else body}</section>")
    add_section("Profile", [d.get("summary")] if d.get("summary") else [])
    for key, title in [("experience","Experience"),("education","Education"),("skills","Skills"),("projects","Projects"),("certifications","Certifications"),("languages","Languages")]:
        add_section(title, d.get(key, []))
    style = "body{font:10pt Arial;color:#202938;margin:36px}h1{font-size:25pt;margin:0}h2{font-size:12pt;color:#315b83;border-bottom:1px solid #ccd5df;padding-bottom:4px;text-transform:uppercase}.sub{color:#526477;margin:5px 0}.entry{margin:9px 0}.entry span{float:right;color:#667085}.entry p{margin:3px 0;color:#475467;white-space:pre-wrap}li{margin:3px 0}"
    return f"<html><meta charset='utf-8'><style>{style}</style><h1>{name}</h1><div><b>{headline}</b></div><div class='sub'>{contact}</div>{''.join(sections)}</html>"

def export_pdf(cv):
    html = sections_html(cv)
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{cv.title.replace(" ", "_")}.pdf"'
    return response

def export_docx(cv):
    d = clean(cv.data); p = d.get("personal", {})
    doc = Document()
    doc.add_heading(p.get("name") or cv.title, 0)
    if p.get("headline"): doc.add_paragraph(p["headline"])
    contact = " | ".join(str(p.get(k)) for k in ("email","phone","location","website") if p.get(k))
    if contact: doc.add_paragraph(contact)
    if d.get("summary"):
        doc.add_heading("Profile", level=1); doc.add_paragraph(str(d["summary"]))
    for key, title in [("experience","Experience"),("education","Education"),("skills","Skills"),("projects","Projects"),("certifications","Certifications"),("languages","Languages")]:
        rows = d.get(key, [])
        if not rows: continue
        doc.add_heading(title, level=1)
        for item in rows:
            if isinstance(item, str): doc.add_paragraph(item, style="List Bullet")
            else:
                heading = item.get("role") or item.get("degree") or item.get("name") or item.get("title") or ""
                sub = item.get("company") or item.get("institution") or item.get("issuer") or item.get("organization") or ""
                para = doc.add_paragraph()
                para.add_run(str(heading)).bold = True
                if sub: para.add_run(" — " + str(sub))
                if item.get("dates"): para.add_run("  |  " + str(item["dates"]))
                if item.get("description"): doc.add_paragraph(str(item["description"]))
    stream = BytesIO(); doc.save(stream); stream.seek(0)
    response = HttpResponse(stream.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    response["Content-Disposition"] = f'attachment; filename="{cv.title.replace(" ", "_")}.docx"'
    return response
