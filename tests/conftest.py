from hypothesis import HealthCheck, Verbosity, settings

settings.register_profile(
    "ci",
    max_examples=100,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.large_base_example],
    deadline=100000,
)
settings.register_profile(
    "dev",
    max_examples=1,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.large_base_example],
    deadline=100000,
)
settings.register_profile(
    "debug",
    max_examples=10,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.large_base_example],
    deadline=100000,
    verbosity=Verbosity.verbose,
)
