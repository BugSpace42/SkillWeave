# profiles/management/commands/seed_skills.py
from django.core.management.base import BaseCommand
from profiles.models import Skill


class Command(BaseCommand):
    help = 'Создает начальные навыки'

    def handle(self, *args, **kwargs):
        hard_skills = [
            'Python', 'JavaScript', 'Java', 'C++', 'SQL', 'HTML/CSS',
            'React', 'Django', 'Flask', 'Node.js', 'TypeScript', 'Git',
            'Docker', 'Kubernetes', 'AWS', 'Data Analysis', 'Machine Learning',
            'Photoshop', 'Figma', 'Adobe Illustrator', 'UI/UX Design',
            'Project Management', 'Agile', 'Scrum', 'Product Management',
            'Digital Marketing', 'SEO', 'SMM', 'Content Writing',
            'Sales', 'Negotiation', 'Customer Service'
        ]

        soft_skills = [
            'Коммуникабельность', 'Работа в команде', 'Лидерство',
            'Решение проблем', 'Критическое мышление', 'Креативность',
            'Адаптивность', 'Эмпатия', 'Тайм-менеджмент',
            'Организованность', 'Внимание к деталям', 'Стрессоустойчивость',
            'Обучаемость', 'Ответственность', 'Самостоятельность',
            'Презентационные навыки', 'Навыки переговоров', 'Конфликтология'
        ]

        for skill_name in hard_skills:
            Skill.objects.get_or_create(
                name=skill_name,
                skill_type='hard',
                defaults={'description': f'Hard skill: {skill_name}'}
            )

        for skill_name in soft_skills:
            Skill.objects.get_or_create(
                name=skill_name,
                skill_type='soft',
                defaults={'description': f'Soft skill: {skill_name}'}
            )

        self.stdout.write(self.style.SUCCESS('Навыки успешно созданы'))