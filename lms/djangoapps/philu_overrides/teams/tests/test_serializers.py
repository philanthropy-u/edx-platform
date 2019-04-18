from lms.djangoapps.teams.tests.factories import CourseTeamFactory
from xmodule.modulestore.tests.factories import CourseFactory
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from lms.djangoapps.philu_overrides.teams.serializers import CustomCourseTeamCreationSerializer


class CreateTeamsSerializerTestCase(ModuleStoreTestCase):
    """
        Tests for the create team serializer.
    """
    def setUp(self):
        super(CreateTeamsSerializerTestCase, self).setUp()
        org = 'edX'
        course_number = 'CS101'
        course_run = '2015_Q1'
        display_name = 'test course 1'

        course = CourseFactory.create(
            org=org,
            number=course_number,
            run=course_run,
            display_name=display_name,
            default_store=ModuleStoreEnum.Type.split,
            teams_configuration={
                "max_team_size": 10,
                "topics": [{u'name': u'T0pic', u'description': u'The best topic!', u'id': u'0'}]
            }
        )
        course.save()
        self.team = CourseTeamFactory.create(
            course_id=course.id,
            topic_id=course.teams_topics[0]['id'],
            name='Test Team',
            description='Testing Testing Testing...',
        )

    def test_create_team_empty_language_field_case(self):
        self.team.country = 'LA'
        data = self.team.__dict__
        expected_result = {'language': ['Language field is required']}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)

    def test_create_team_invalid_language_code_case(self):
        self.team.country = 'LA'
        self.team.language = 'klkl'
        data = self.team.__dict__
        expected_result = {'language': ['klkl is not a valid language code']}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)

    def test_create_team_empty_country_field_case(self):
        self.team.language = 'kl'
        data = self.team.__dict__
        expected_result = {'country': ['Country field is required']}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)

    def test_create_team_invalid_country_code_case(self):
        self.team.country = 'LALA'
        self.team.language = 'kl'
        data = self.team.__dict__
        expected_result = {'country': ['LALA is not a valid country code']}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)

    def test_create_team_both_empty_fields_case(self):
        data = self.team.__dict__
        expected_result = {'country': ['Country field is required'], 'language': ['Language field is required']}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)

    def test_create_team_both_invalid_code_case(self):
        self.team.country = 'LALA'
        self.team.language = 'klkl'
        data = self.team.__dict__
        expected_result = {'country': ['LALA is not a valid country code'], 'language': ['klkl is not a valid language code']}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)

    def test_create_team_valid_code_case(self):
        self.team.country = 'LA'
        self.team.language = 'kl'
        data = self.team.__dict__
        expected_result = {}
        serialized_data = CustomCourseTeamCreationSerializer(data=data)
        serialized_data.is_valid()
        self.assertEqual(serialized_data.errors, expected_result)
