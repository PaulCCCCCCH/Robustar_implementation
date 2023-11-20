def pytest_addoption(parser):
    parser.addoption(
        "--data_path",
        action="store",
        default="/Robustar2-test",
        help="Path of the test data",
    )
