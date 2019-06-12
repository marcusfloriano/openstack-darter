

from src.darter import Openstack


def test_domain():
    os = Openstack()
    os.domains("packstack")


def test_total_of_compute():
    openstack = Openstack()
    total = openstack.total_of_compute("packstack")
    assert "total_cores_used" in total
    assert "total_instances_used" in total
    assert "total_ram_used" in total
    assert "max_total_cores" in total
    assert "max_total_instances" in total
    assert "max_total_ram_size" in total
    assert total["max_total_cores"] > 0
