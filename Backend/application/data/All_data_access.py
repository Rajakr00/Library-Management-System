from flask import jsonify
from application.data.model import user, Section, Ebook

def get_all_section():
    sections = Section.query.all()
    sections_list =[]
    for sec in sections :
        sections_list.append({"section_id":sec.section_id,"section_name":sec.section_name,"section_description":sec.section_description})
    return sections_list
    

def get_all_ebook():
    ebooks = Ebook.query.all()
    ebooks_list =[]
    for ebook_s in ebooks :
        ebooks_list.append({"ebook_id":ebook_s.ebook_id,"name":ebook_s.name,"content":ebook_s.content,"authors":ebook_s.authors,"section_id":ebook_s.section_id})
    return ebooks_list