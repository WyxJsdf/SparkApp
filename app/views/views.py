# -*- coding: utf-8 -*-
__author__ = 'wangbb13'

from flask import Blueprint, render_template, redirect, url_for, \
                  request, flash, g, json, jsonify
from .scenes import scene2
import pickle

mod = Blueprint('views', __name__)

@mod.route('/')
def index():
  return render_template('scenes.html')

@mod.route('/<int:scene>')
def scenes(scene):
  scene = int(scene)
  print(scene)
  if scene == 2:
    try:
      day_info, quarter_info, year_info = pickle.load(open("scene2_data.pkl", "rb"))
    except:
      lines = scene2.get_lines()
      day_data, quarter_data, year_data = scene2.statistic_scene2(lines)
      day_info = []
      quarter_info = []
      year_info = []
      for k, v in day_data:
        day_info.append(k.year)
        day_info.append(k.month)
        day_info.append(k.day)
        day_info.append(v[0])
        day_info.append(int(v[1]))
      for k, v in quarter_data:
        quarter_info.append(k.year)
        quarter_info.append(k.month)
        quarter_info.append(k.day)
        quarter_info.append(v[0])
        quarter_info.append(int(v[1]))
      for k, v in year_data:
        year_info.append(k.year)
        year_info.append(k.month)
        year_info.append(k.day)
        year_info.append(v[0])
        year_info.append(int(v[1]))
      day_info = json.dumps(day_info)
      quarter_info = json.dumps(quarter_info)
      year_info = json.dumps(year_info)
      with open("scene2_data.pkl", "wb") as f:
        pickle.dump((day_info, quarter_info, year_info), f)
    return jsonify(day_info, quarter_info, year_info)
  else:
    return render_template('scenes.html')
