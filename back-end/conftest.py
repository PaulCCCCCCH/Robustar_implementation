def pytest_addoption(parser):
    parser.addoption(
        "--zip_file_path",
        action="store",
        default="/Robustar2-test.zip",
        help="Path of the zipped test folder",
    )
