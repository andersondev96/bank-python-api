# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch, Mock
import pytest
from src.controllers.factory import ControllerFactory
from src.models.sqlite.settings.connection import DBConnectionHandler

@pytest.fixture
def mock_db_connection_handler():
    mock = MagicMock(spec=DBConnectionHandler)
    mock.__enter__.return_value = mock
    mock.__exit__.return_value = None
    mock.connection_to_db.return_value = None

    mock.session = MagicMock()
    mock.session.query.return_value.filter.return_value.one.return_value = None
    return mock


@pytest.fixture
def mock_pf_repository():
    return MagicMock()


@pytest.fixture
def mock_pj_repository():
    return MagicMock()


class TestControllerFactory:

    def test_criar_pessoa_fisica_controller(self, mock_db_connection_handler):
        controller = ControllerFactory.criar_pessoa_fisica_controller(mock_db_connection_handler)
        assert controller is not None
        assert hasattr(controller, 'repository')

    def test_criar_pessoa_juridica_controller(self, mock_db_connection_handler):
        controller = ControllerFactory.criar_pessoa_juridica_controller(mock_db_connection_handler)
        assert controller is not None
        assert hasattr(controller, 'repository')

    @patch('src.controllers.factory.PessoaFisicaRepository')
    @patch('src.controllers.factory.PessoaJuridicaRepository')
    def test_criar_todos(self, mock_pj_repo_class, mock_pf_repo_class):
        mock_pf_repo_instance = Mock()
        mock_pj_repo_instance = Mock()

        mock_pf_repo_class.return_value = mock_pf_repo_instance
        mock_pj_repo_class.return_value = mock_pj_repo_instance

        controllers = ControllerFactory.criar_todos()

        mock_pf_repo_class.assert_called_once()
        mock_pj_repo_class.assert_called_once()

        assert "pessoa_fisica" in controllers
        assert "pessoa_juridica" in controllers
        assert "db_connection" in controllers
        assert controllers["pessoa_fisica"].repository == mock_pf_repo_instance
        assert controllers["pessoa_juridica"].repository == mock_pj_repo_instance
