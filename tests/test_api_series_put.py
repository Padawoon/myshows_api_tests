import psycopg
import pytest
import allure
from http import HTTPStatus
from config.api_config import BASE_URL
from data.api_endpoints import SERIES
from pytest_check import check
from fixtures.prepare_data_fixtures import DB_CONFIG


@allure.suite("API MyShows/Series: Обновление сериалов")
class TestPutSeries:
    @allure.title("Успешное обновление поля '{field}' сериала")
    @pytest.mark.positive
    @pytest.mark.parametrize("field, new_value", [
        ("name", "Новый сериал"),
        ("rating", 3),
        ("status", "watched"),
        ("review", "Новый отзыв"),
        ("photo", "https://kinopoisk-ru.clstorage.net/1B5y2x231/318d8boZz4T/deonbbaqSdMCKs80awYCCf40QuBho9WmZXCB6XOXWVJBcIxacbZhyikF7oYO8Ca-OS_y9b9xPbEEAtClr_QtA_Vus_pkbJ7EFayfYfxGVxm4N4Mw5nHAN2I0Vr-kXJVYTfrQ0_58acExVH1Vi2Tyq-k_ZTb6JvvgQB5Jdf2yttT4JiEluXoMFIfyD33ixgYEZTrJrH5kVal2-M7meh5R28fzXZPwcKZNNtr9mBsjeyGium_-vKWprIQdDOP4fz3Qt-JnbbD9Tl-L9Mf3LASFwuE1i-Y8LpQv_TPB6jMY2ZnBfBlT-HesAjea-BbVLfiiIHUseTit7mqMm8Rst3C2lDfu7SW5coSURLIAsKSLQA6vtkntuaMXbfb-hSY4k5IYQ__b2bk6Y0K5kfRRnGZ8aq4yqnF4aaTmidhOJjU6_5L-JSOqe3lG2M6ygj3pwsVO6HcN77zi0G9yvEMptd4TUgM501QwP6pJelzw2JLueaxreqB1viCrbARZDmxxv7jSf2GlaDgzilcAeIB_aY0Aj2w8yWS2pFHn9nZCK_MQX1nJcNlTs7flgDabOlTbojJs7nAjt3rnquyBkI0gvjE8l7Ujo-h__8bbA7XMfuBHQEamOsDk9CMcbTBzxy59lt7cA_6c2Xk-qkGw2jVR2CC6aWi-JfB8Ju4oTpwGZ3a_MhY7K2EkPrAK1oYxxzpuhgvOpPtPbblpGGE7swiqsdAZWg74GZz0tqJLsJuyGNEktSNptm88864m4MHUAuYy-D9bvOzt7PjxBJtM8kv_bAwIimA7SiWxrxqofnOOqLNb3NWD81eSMjItADhVelNbZzZrpLEqvbjlI24GGUTneDG2FfPurWT-ugYex3NM_eYLSwMh94nmMC9aZTS6x241VdncRvLTXLkzaYm2E7HZkqM1ZG8w4_E_ZmFuh9RM5vHxNh_5oWZosbfM3A_yQLesQwqLbftO4z9rFad4eIak9FFaHIGxnhy-8G1B-5oyUBQvfKpvPiK5fq4h5IMShKw6fHRcfe9mqzI4hBEOsER4bgWNCeizyGF06Z9nNP5FJ_DW2dNB8JNbsjMliTybedRZr7QrYjXt_Xas4-yGn8Cnvv0237TlJGR0f4GTgzIFtaGLhUXpfIfp_uHQo_s6w-B0WdTah_LdHjq8qQPyEHzRE6O0Iia_r3c6aCumR5jI6f90Np29ba0if3iL34Uwj_ghwUaCJ7VL5nzgHCoy-oqhedrZVEHxFplzfOCP8pwz2dsre6qk-utw_2RqKoMahyx7Of0beSan73MyjNOGs4k_Y4wPCW53h-s045Yl9HYKpLWblNsJOhJTuTxhg_ZZdFUQb7aiqf1ssLOhq21I0sglOfa63rXhLWB4-soUjLfN9-GPyYKv-cavcawS4Hq2w-G9GVnSAP4TFfs8KkB6nHsa3Ca5red5KPb1qSWuBlIApjF--N98b-ltdn1PWANxw3KhDUIE538GaHum0af7cEbnfNsWWUGw1pxye6mPNtz82NiveG0m-qIwsy_iJc_UymV3eXPTMy5krDI8BhcEc0n37IoAzCa3gWw4LtXmu_cCaLmbFlhNfpWWsH-pT3_YM5oW4L7r6LOs8DWqpC8OVE7mMHh1HXkqYii6uwMfxz3BMmQBiE0kdYYo9O8Qq707TaCzXV8SBj_SGjP_YM1xnTKeGKa5JaC9Y7a9ZqXmSN_DK7H9OB80JGZp_jIDlwR0QD9rQ4lKYPyPJ_ijmCnwOgAiO99bm834Hp44cKBPOlf11ZWqsWlmNue9taKmLAEVByN-fb0Wt-duYvC3QxaN80c-LYZPTCY-z6G-LJLqdnzArzGTnxTPsJlWf3whj_hRMVSUrzahabBs_DXhISdDEIDn8jAwFzAtI-v590heT3mCteYNSk-rs0amsWxRab0wTeo8mNlSBvvUWPH24Q_5V7FVle24ru85q3B-riTowJhEJTJy89685SGvsbrPVg3yybxtxUvL5fnCZHEgGGO-f8ZuulHbHMD20xT5N2XGMNk5HJOovS4geu89fyikacUbTaN3_naX-WeqZz7_iZqHM4dyoUsIjO67z294KlUv8nYC4DAe19VFc1maeH8jATMY85Ha7fMk67OkP33vYiRL2wIs83q41jUrrWlwuIicSHLMfKlJio4ofgNgP6CfoHewBSqyGdmdCPDWUnI4ZYM20Pbb06x4Y2myYv8_JOVvSdiILLk9O5u_qi_r_3WAl8WxgPVqTULJrj3BLj5hkWi0s40k_ZZf0048WpBwf6RI8xBzFBos-irpuChxPiFgKEBQgiu_tnrQs6ZtKzd4T1GF_EDwoA_AyiQ7S-i_YFglMzZNrvKV0BVBsR9efr-hxXRYc9uRJ_1p7jFvdT2hrGlAE4_kMj3yXzuk6q22usORQ7MAP-NPRoWv94CjMGwfIvX7yCG20tzZS_CfUnO3bQq8kXsTW6d7bmtwZPb8bKUpgx1M6Lj9tBr-aiTsPPgOUs-9gH4oBU8J7HOAKDtv0Wc9NkfosRYeHEcyn9U29qIPPJJ6UJylfunjvmN4O-ciKsWSCK449b-Y--6qpbo3g9eKeYn84UJJCyB5QK94YB5gv7ONoLYX01tFdpdS9jbmRvfTMRITrzHiIL0t-PdtrO5PWQVoPrq_H7wqLOW_tYNQxbVAf6bHg4Gss0rsu2jeazu8R6F0VlbQgHhZUzk06QC6m3sd02ixbGc6bb-67ePlQ9EFbv2yuNV55Kqr-P1LHg0wwr6sTMVFL_GN7_cp3q46sMFhNlbaHI98GlpxuCXPOFj5GNIgtK2g8ia_c6ft5ItRDig-8npSeKkqIDczitjEOcd3LgOOS6X3B-N7IlggtL4NrjUX2BZOcRfSuzumjvCdtptSarol4bJg-rvlLunPmQvof7R_kLDiJC8xMIyShzwDdeKFC4HnNoou_iSZ6jq0yuk83p4ehXIS1XIz4kJ507XVlWB57GR-77Y_oiGlRI")
    ],
    ids=["change_name", "change_rating", "change_status", "change_review", "change_photo"]
    )
    def test_update_series_success(self, api_client, input_and_yield_one_show, field, new_value):
        with allure.step("Подготовка тестовых данных и получение ID"):
            show_id = input_and_yield_one_show
        with allure.step(f"Формирование payload для обновления поля '{field}'"):
            payload = {"name": "Тестовый сериал",
                       "photo": "https://avatars.mds.yandex.net/get-kinopoisk-image/1898899/20df477e-8a1c-4cf3-8518-7873e196ab60/300x450",
                       "rating": 10, "status": "watching", "review": "Тестовое описание", field: new_value}
        with allure.step("Отправка PUT-запроса на обновление сериала"):
            response = api_client.put(
                f"{BASE_URL}{SERIES}/{show_id}",
                json=payload
            )
        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == HTTPStatus.OK

        with allure.step("Проверка обновленного значения в базе данных"):
            with psycopg.connect(**DB_CONFIG) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT {field} FROM series where id = %s;", (show_id,))
                    db_res = cur.fetchone()

            check.equal(db_res[0], new_value)

        # Тут я сначала сделал e2e проверку через гет, но потом переосмыслил ТЗ и понял, что нужно именно через бд
        # response = api_client.get(
        #     f"{BASE_URL}{SERIES}/{show_id}"
        # )
        # response_body = response.json()
        # check.equal(response_body[field], new_value)