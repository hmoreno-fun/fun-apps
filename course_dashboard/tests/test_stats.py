from datetime import datetime

from django.test.utils import override_settings
from django.utils import timezone

from student.tests.factories import CourseEnrollmentFactory
from xmodule.modulestore.tests.factories import CourseFactory

import course_dashboard.stats as stats
from .base import BaseCourseDashboardTestCase


class StatsTestCase(BaseCourseDashboardTestCase):

    def test_population_by_country_for_empty_course(self):
        course = CourseFactory.create()
        course_population = stats.population_by_country(self.get_course_id(course))
        self.assertEqual({}, course_population)

    def test_population_by_country_for_non_empty_course(self):
        course = CourseFactory.create()
        empty_course = CourseFactory.create()
        course_id = self.get_course_id(course)
        empty_course_id = self.get_course_id(empty_course)
        CourseEnrollmentFactory.create(course_id=course_id, user__profile__country='FR')

        empty_course_population = stats.population_by_country(empty_course_id)
        course_population = stats.population_by_country(course_id)

        self.assertEqual({}, empty_course_population)
        self.assertEqual({'FR': 1}, course_population)

    def test_non_active_students_not_included(self):
        course = CourseFactory.create()
        self.enroll_student(course, user__profile__country='FR', user__is_active=False)
        course_population = stats.population_by_country(self.get_course_id(course))
        self.assertEqual({}, course_population)

    @override_settings(TIME_ZONE=timezone.UTC())
    def test_enrollments_per_month(self):
        course = CourseFactory.create()
        # Note that date parsing is not supposed to work for timezones other
        # than UTC
        self.enroll_student_at(course, 2013, 12, 31)
        self.enroll_student_at(course, 2014, 1, 14)
        self.enroll_student_at(course, 2014, 1, 31)
        self.enroll_student_at(course, 2014, 2, 1)
        self.enroll_student_at(course, 2014, 3, 1, user__is_active=False)
        since = datetime(2014, 1, 1, tzinfo=timezone.UTC())

        enrollments = stats.enrollments_per_month(self.get_course_id(course), since=since)
        self.assertEqual([(datetime(2014, 1, 1), 2), (datetime(2014, 2, 1), 1)], enrollments)

    def enroll_student_at(self, course, year, month, day, **kwargs):
        # For some reason, the course enrollment factory does not set the
        # proper creation date so we need to set it manually
        enrollment = self.enroll_student(course, **kwargs)
        enrollment.created = datetime(year, month, day, tzinfo=timezone.UTC())
        enrollment.save()
