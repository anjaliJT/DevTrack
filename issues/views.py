from django.shortcuts import render


import json
from django.http import JsonResponse
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue
from .utils import read_json, write_json

def create_reporter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            reporter = Reporter(**data)
            reporter.validate()

            reporters = read_json('reporters.json')
            reporters.append(reporter.to_dict())
            write_json('reporters.json', reporters)

            return JsonResponse(reporter.to_dict(), status=201)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
            
# Create your views here.


def get_reporters(request):
    reporters = read_json('reporters.json')
    reporter_id = request.GET.get('id')

    if reporter_id:
        for r in reporters:
            if r['id'] == int(reporter_id):
                return JsonResponse(r, status=200)
        return JsonResponse({'error': 'Reporter not found'}, status=404)

    return JsonResponse(reporters, safe=False)

def get_issues(request):
    issues = read_json('issues.json')

    issue_id = request.GET.get('id')
    status = request.GET.get('status')

    if issue_id:
        for issue in issues:
            if issue['id'] == int(issue_id):
                return JsonResponse(issue, status=200)
        return JsonResponse({'error': 'Issue not found'}, status=404)

    if status:
        filtered = [i for i in issues if i['status'] == status]
        return JsonResponse(filtered, safe=False)

    return JsonResponse(issues, safe=False)


def create_issue(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            if data['priority'] == 'critical':
                issue = CriticalIssue(**data)
            elif data['priority'] == 'low':
                issue = LowPriorityIssue(**data)
            else:
                issue = Issue(**data)

            issue.validate()

            issues = read_json('issues.json')
            issue_data = issue.to_dict()
            issue_data['message'] = issue.describe()

            issues.append(issue_data)
            write_json('issues.json', issues)

            return JsonResponse(issue_data, status=201)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)