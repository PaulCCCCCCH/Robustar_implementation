def pytest_addoption(parser):
    parser.addoption("--basedir", action="store", default="/", help="Base directory where the robustar test folder is unzipped")



