# Task 6 - duplicates after the nightly import
#
# 6.1 If a class has no __eq__ and __hash__, == compares identity (is) and
#     hash() is made from the object id. Two Student objects with the same
#     data are two different objects, so the set keeps both.
# 6.2 When a class defines only __eq__, python sets __hash__ = None, so the
#     object becomes unhashable and set.add gives TypeError.
# 6.3 Same student = same student_id. Name and group can change (a student
#     can move SE-31 -> SE-32 and it is still the same person), the id can't.
#     So __eq__ and __hash__ use only student_id.
# 6.4 If the hash uses group, then after s.group changes the set looks in a
#     wrong bucket and can not find the student (see BadStudent and its test).
# 6.5 @dataclass(frozen=True) compares and hashes ALL fields, so group is
#     included too and a student with a new group is a different student.
#     Also frozen means we can't even change the group. We would need
#     field(compare=False) for name and group, but then frozen blocks the move.
# 6.6 __repr__ is below.


class Student:
    def __init__(self, student_id, full_name, group):
        self.student_id = student_id
        self.full_name = full_name
        self.group = group

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.student_id == other.student_id

    def __hash__(self):
        return hash(self.student_id)

    def __repr__(self):
        return f"Student(student_id={self.student_id!r}, group={self.group!r})"


# wrong idea from 6.4, only for the demo
class BadStudent:
    def __init__(self, student_id, group):
        self.student_id = student_id
        self.group = group

    def __eq__(self, other):
        return self.group == other.group

    def __hash__(self):
        return hash(self.group)


def test_import_loop_prints_one():
    seen = set()
    for row in [("U2310045", "Ali Valiyev", "SE-31"),
                ("U2310045", "Ali Valiyev", "SE-31")]:
        seen.add(Student(*row))
    assert len(seen) == 1


def test_found_after_group_change():
    s = Student("U2310045", "Ali Valiyev", "SE-31")
    seen = {s}
    s.group = "SE-32"
    assert s in seen
    # csv with the new group is still the same student
    assert Student("U2310045", "Ali Valiyev", "SE-32") in seen


def test_different_ids_are_different():
    assert Student("U1", "A", "SE-31") != Student("U2", "A", "SE-31")


def test_equal_objects_have_equal_hash():
    a = Student("U1", "A", "SE-31")
    b = Student("U1", "B", "SE-32")
    assert a == b
    assert hash(a) == hash(b)


def test_not_equal_to_other_type():
    assert Student("U1", "A", "SE-31") != "U1"


def test_repr():
    s = Student("U2310045", "Ali Valiyev", "SE-31")
    assert repr(s) == "Student(student_id='U2310045', group='SE-31')"


def test_hash_by_group_is_bad():
    s = BadStudent("U1", "SE-31")
    seen = {s}
    s.group = "SE-32"
    assert s not in seen  # lost, the bug
