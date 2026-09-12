"""Optional development seeding entrypoint.

Production records are created through authenticated APIs. This script intentionally
does not create default credentials.
"""


def main() -> None:
    print("No default data is required. Register a user through POST /api/v1/auth/register.")


if __name__ == "__main__":
    main()
