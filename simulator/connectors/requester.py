from simulator.utils import do_request, compare_dict
from simulator.models import State, Case


class CaseRequests:
    def __init__(self, debug=False):
        self.debug = debug

    def run_tests(self, case_ids=None):
        cases = Case.objects.filter(active=True)
        if case_ids:
            cases = cases.filter(id__in=case_ids)
        for test_case in cases.all():
            project = test_case.project

            State.set_case(test_case)
            # need_output_file = False
            # if "file" in test_case.get("front", {}).get("response", {}):
            #     need_output_file = True
            if self.debug:
                print("start ------------------------------------->")
                print("> Request", test_case)

            code, result = do_request(
                test_case.out_request_method,
                f"{project.location()}{test_case.out_url_path}",
                headers=project.get_headers(),
                data=test_case.out_request_body,
                debug=self.debug,
                # raw_result=need_output_file,
            )

            # if need_output_file:
            #     with open(test_case["front"]["response"]["file"], "wb") as file:
            #         file.write(result)

            if self.debug:
                print("Plan Result", test_case.out_response_code, test_case.out_response_body)
                print("Real Result", code, result)

            checked = self.check(code, result, test_case)
            if self.debug:
                print("end ---------------------------------------<")

            print(f"Case: {test_case} -> {'OK' if checked else 'ERROR'}")

    def check(self, code, result, test_case):
        checked, checked2 = True, True
        case_body = test_case.out_response_body
        if test_case.out_response_code is not None and code != test_case.out_response_code:
            print(f'>> CODE MISMATCH: {code} != {test_case.out_response_code}')
            checked = False

        if case_body is not None:
            checked2 = compare_dict(case_body, result, self.debug)

        return checked and checked2
