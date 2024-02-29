# run pytest with --hypothesis-profile=dev to load a profile

from hypothesis import HealthCheck, Verbosity, settings

settings.register_profile(
    "push",
    max_examples=1,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
)
settings.register_profile(
    "pull_request",
    max_examples=50,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
)
settings.register_profile(
    "pre_release",
    max_examples=100,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
)
settings.register_profile(
    "dev",
    max_examples=1,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
    verbosity=Verbosity.verbose,
    print_blob=True,
)
settings.register_profile(
    "debug",
    max_examples=10,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.large_base_example,
        HealthCheck.data_too_large,
    ],
    deadline=100000,
    verbosity=Verbosity.verbose,
    print_blob=True,
)