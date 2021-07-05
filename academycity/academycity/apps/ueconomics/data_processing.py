from django.conf import settings
import pandas as pd
import numpy as np
import math
from openpyxl.utils.dataframe import dataframe_to_rows
import csv
import pickle
from openpyxl import Workbook, load_workbook
from ..core.algo_utilities import Algo
from .models import Source, Product, YearData


class AlgoUE(Algo):
    def __init__(self):
        super().__init__(chapter_id="ueconomics", target_field=None)

    def upload_data_to_database(self):
        df_exports = self.load_excel_data('exports')
        df_imports = self.load_excel_data('imports')
        Source.truncate()
        Product.truncate()
        source_exports, created = Source.objects.get_or_create(type='exports')
        if created:
            for index, row in df_exports.iterrows():
                description_ = row['Description']
                sitc2_ = row['SITC2']
                product, created = Product.objects.get_or_create(sitc2=sitc2_, description=description_)
                for ny in range(2015, 2020):
                    y = 'Y' + str(ny)
                    v = row[y]
                    yd, created = YearData.objects.get_or_create(source=source_exports, product=product, year=ny,
                                                                 value=v)

            source_imports, created = Source.objects.get_or_create(type='imports')
            for index, row in df_imports.iterrows():
                description_ = row['Description']
                sitc2_ = row['SITC2']
                product, created = Product.objects.get_or_create(sitc2=sitc2_, description=description_)
                for ny in range(2015, 2020):
                    y = 'Y' + str(ny)
                    v = row[y]
                    yd, created = YearData.objects.get_or_create(source=source_imports, product=product, year=ny,
                                                                 value=v)

