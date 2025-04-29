<p><b>CLI-приложение для анализа логов Django.</b> <br>Формирует отчет и выводит его в консоль.</p>
<p>python3 main.py [file lists] [--report report name]</p>
<p>Опции:</p>
<ul>
<li>file lists: список лог-файлов</li>
<li>--report report name: где report name - наименование отчета.</li>
</ul>
<p>Пример:<br>
python3 main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
</p>
<p>На текущий момент реализован отчет с наименованием <code>handlers</code>,
<br>который считает количество запросов к handler для записей django.requests из указанных файлов
</p>
<p>
<img src="https://github.com/Needlees/Django_handlers_report2/blob/master/img/example.png" width="525" style="max-width: 100%">
</p>
<p>Для добавления нового отчета необходимо добавить реализацию абстрактного класса <code>ReportTable</code> в <code>report.py</code><br>
и добавить созданный класс вместе с наименованием для CLI в нижеприведенный словарь:</p>
<pre>
REPORTS: dict[str, Type[reports.ReportTable]] = {
    'handlers': reports.HandlersReport
}
</pre>
