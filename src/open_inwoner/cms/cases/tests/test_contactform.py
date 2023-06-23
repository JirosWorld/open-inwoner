from django.test import override_settings
from django.urls import reverse
from django.utils.translation import gettext as _

import requests_mock
from django_webtest import WebTest
from zgw_consumers.api_models.constants import (
    RolOmschrijving,
    RolTypes,
    VertrouwelijkheidsAanduidingen,
)
from zgw_consumers.constants import APITypes
from zgw_consumers.test import generate_oas_component, mock_service_oas_get

from open_inwoner.accounts.tests.factories import DigidUserFactory
from open_inwoner.openklant.constants import Status
from open_inwoner.openklant.models import OpenKlantConfig
from open_inwoner.openklant.tests.data import (
    CONTACTMOMENTEN_ROOT,
    KLANTEN_ROOT,
    MockAPIData,
)
from open_inwoner.openzaak.models import OpenZaakConfig
from open_inwoner.openzaak.tests.factories import (
    ServiceFactory,
    ZaakTypeConfigFactory,
    ZaakTypeInformatieObjectTypeConfigFactory,
)
from open_inwoner.openzaak.tests.shared import (
    CATALOGI_ROOT,
    DOCUMENTEN_ROOT,
    ZAKEN_ROOT,
)
from open_inwoner.utils.test import ClearCachesMixin, paginated_response


@requests_mock.Mocker()
@override_settings(ROOT_URLCONF="open_inwoner.cms.tests.urls")
class ContactFormTestCase(ClearCachesMixin, WebTest):
    def setUp(self):
        super().setUp()

        self.user = DigidUserFactory(bsn="900222086")

        # services
        self.zaak_service = ServiceFactory(api_root=ZAKEN_ROOT, api_type=APITypes.zrc)
        self.catalogi_service = ServiceFactory(
            api_root=CATALOGI_ROOT, api_type=APITypes.ztc
        )
        self.document_service = ServiceFactory(
            api_root=DOCUMENTEN_ROOT, api_type=APITypes.drc
        )
        # openzaak config
        self.oz_config = OpenZaakConfig.get_solo()
        self.oz_config.zaak_service = self.zaak_service
        self.oz_config.catalogi_service = self.catalogi_service
        self.oz_config.document_service = self.document_service
        self.oz_config.document_max_confidentiality = (
            VertrouwelijkheidsAanduidingen.beperkt_openbaar
        )
        self.oz_config.zaak_max_confidentiality = (
            VertrouwelijkheidsAanduidingen.beperkt_openbaar
        )
        self.oz_config.save()

        # openklant config
        self.ok_config = OpenKlantConfig.get_solo()
        self.ok_config.register_contact_moment = True
        self.ok_config.register_bronorganisatie_rsin = "123456788"
        self.ok_config.register_type = "Melding"
        self.ok_config.register_employee_id = "FooVonBar"
        self.ok_config.klanten_service = ServiceFactory(
            api_root=KLANTEN_ROOT, api_type=APITypes.kc
        )
        self.ok_config.contactmomenten_service = ServiceFactory(
            api_root=CONTACTMOMENTEN_ROOT, api_type=APITypes.cmc
        )
        self.ok_config.save()

        self.zaak = generate_oas_component(
            "zrc",
            "schemas/Zaak",
            uuid="d8bbdeb7-770f-4ca9-b1ea-77b4730bf67d",
            url=f"{ZAKEN_ROOT}zaken/d8bbdeb7-770f-4ca9-b1ea-77b4730bf67d",
            zaaktype=f"{CATALOGI_ROOT}zaaktypen/0caa29cb-0167-426f-8dc1-88bebd7c8804",
            identificatie="ZAAK-2022-0000000024",
            omschrijving="Zaak naar aanleiding van ingezonden formulier",
            startdatum="2022-01-02",
            einddatum=None,
            status=f"{ZAKEN_ROOT}statussen/3da89990-c7fc-476a-ad13-c9023450083c",
            resultaat=f"{ZAKEN_ROOT}resultaten/a44153aa-ad2c-6a07-be75-15add5113",
            vertrouwelijkheidaanduiding=VertrouwelijkheidsAanduidingen.openbaar,
        )
        self.user_role = generate_oas_component(
            "zrc",
            "schemas/Rol",
            url=f"{ZAKEN_ROOT}rollen/f33153aa-ad2c-4a07-ae75-15add5891",
            omschrijvingGeneriek=RolOmschrijving.initiator,
            betrokkeneType=RolTypes.natuurlijk_persoon,
            betrokkeneIdentificatie={
                "inpBsn": "900222086",
                "voornamen": "Foo Bar",
                "voorvoegselGeslachtsnaam": "van der",
                "geslachtsnaam": "Bazz",
            },
        )
        self.zaaktype = generate_oas_component(
            "ztc",
            "schemas/ZaakType",
            uuid="0caa29cb-0167-426f-8dc1-88bebd7c8804",
            url=self.zaak["zaaktype"],
            identificatie="ZAAKTYPE-2020-0000000001",
            omschrijving="Coffee zaaktype",
            catalogus=f"{CATALOGI_ROOT}catalogussen/1b643db-81bb-d71bd5a2317a",
            vertrouwelijkheidaanduiding=VertrouwelijkheidsAanduidingen.openbaar,
            indicatieInternOfExtern="extern",
        )
        self.zaak_informatie_object = generate_oas_component(
            "zrc",
            "schemas/ZaakInformatieObject",
            url=f"{ZAKEN_ROOT}zaakinformatieobjecten/e55153aa-ad2c-4a07-ae75-15add57d6",
            informatieobject=f"{DOCUMENTEN_ROOT}enkelvoudiginformatieobjecten/014c38fe-b010-4412-881c-3000032fb812",
            zaak=self.zaak["url"],
        )
        self.uploaded_zaak_informatie_object = generate_oas_component(
            "zrc",
            "schemas/ZaakInformatieObject",
            url=f"{ZAKEN_ROOT}zaakinformatieobjecten/48599f76-b524-48e8-be5a-6fc47288c9bf",
            informatieobject=f"{DOCUMENTEN_ROOT}enkelvoudiginformatieobjecten/48599f76-b524-48e8-be5a-6fc47288c9bf",
            zaak=self.zaak["url"],
        )
        self.informatie_object_type = generate_oas_component(
            "ztc",
            "schemas/InformatieObjectType",
            url=f"{CATALOGI_ROOT}informatieobjecttype/014c38fe-b010-4412-881c-3000032fb321",
            catalogus=f"{CATALOGI_ROOT}catalogussen/1b643db-81bb-d71bd5a2317a",
            omschrijving="Some content",
        )
        self.informatie_object = generate_oas_component(
            "drc",
            "schemas/EnkelvoudigInformatieObject",
            uuid="014c38fe-b010-4412-881c-3000032fb812",
            url=self.zaak_informatie_object["informatieobject"],
            inhoud=f"{DOCUMENTEN_ROOT}enkelvoudiginformatieobjecten/014c38fe-b010-4412-881c-3000032fb812/download",
            informatieobjecttype=self.informatie_object_type["url"],
            status="definitief",
            vertrouwelijkheidaanduiding=VertrouwelijkheidsAanduidingen.openbaar,
            bestandsnaam="uploaded_document.txt",
            titel="uploaded_document_title.txt",
            bestandsomvang=123,
        )
        self.status_finish = generate_oas_component(
            "zrc",
            "schemas/Status",
            url=f"{ZAKEN_ROOT}statussen/3da89990-c7fc-476a-ad13-c9023450083c",
            zaak=self.zaak["url"],
            statustype=f"{CATALOGI_ROOT}statustypen/e3798107-ab27-4c3c-977d-744516671fe4",
            datumStatusGezet="2021-03-12",
            statustoelichting="",
        )
        self.status_type_finish = generate_oas_component(
            "ztc",
            "schemas/StatusType",
            url=self.status_finish["statustype"],
            zaaktype=self.zaaktype["url"],
            catalogus=f"{CATALOGI_ROOT}catalogussen/1b643db-81bb-d71bd5a2317a",
            omschrijving="Finish",
            omschrijvingGeneriek="some content",
        )
        self.result = generate_oas_component(
            "zrc",
            "schemas/Resultaat",
            uuid="a44153aa-ad2c-6a07-be75-15add5113",
            url=self.zaak["resultaat"],
            resultaattype=f"{CATALOGI_ROOT}resultaattypen/b1a268dd-4322-47bb-a930-b83066b4a32c",
            zaak=self.zaak["url"],
            toelichting="resultaat toelichting",
        )
        self.klant = generate_oas_component(
            "kc",
            "schemas/Klant",
            uuid="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            url=f"{KLANTEN_ROOT}klant/aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            bronorganisatie="123456789",
            voornaam="Foo",
            achternaam="Bar",
            emailadres="foo@example.com",
            telefoonnummer="0612345678",
        )

        # enable upload and contact moments
        zaak_type_config = ZaakTypeConfigFactory(
            catalogus__url=f"{CATALOGI_ROOT}catalogussen/1b643db-81bb-d71bd5a2317a",
            identificatie=self.zaaktype["identificatie"],
            contact_moments_enabled=True,
        )
        ZaakTypeInformatieObjectTypeConfigFactory(
            zaaktype_config=zaak_type_config,
            informatieobjecttype_url=self.informatie_object["url"],
            zaaktype_uuids=[self.zaaktype["uuid"]],
            document_upload_enabled=True,
        )

        self.case_detail_url = reverse(
            "cases:case_detail_content", kwargs={"object_id": self.zaak["uuid"]}
        )

    def _setUpMocks(self, m):
        mock_service_oas_get(m, ZAKEN_ROOT, "zrc")
        mock_service_oas_get(m, CATALOGI_ROOT, "ztc")
        mock_service_oas_get(m, DOCUMENTEN_ROOT, "drc")
        MockAPIData.setUpOASMocks(m)

        self.matchers = []

        for resource in [
            self.zaak,
            self.result,
            self.zaaktype,
            self.informatie_object,
            self.status_finish,
            self.status_type_finish,
        ]:
            self.matchers.append(m.get(resource["url"], json=resource))

        self.matchers += [
            m.get(
                f"{ZAKEN_ROOT}rollen?zaak={self.zaak['url']}",
                json=paginated_response([self.user_role]),
            ),
            m.get(
                f"{ZAKEN_ROOT}zaakinformatieobjecten?zaak={self.zaak['url']}",
                [
                    {
                        "json": [
                            self.zaak_informatie_object,
                        ]
                    },
                    # after upload
                    {
                        "json": [
                            self.zaak_informatie_object,
                            self.uploaded_zaak_informatie_object,
                        ]
                    },
                ],
            ),
            m.get(
                f"{ZAKEN_ROOT}statussen?zaak={self.zaak['url']}",
                json=paginated_response([self.status_finish]),
            ),
            m.get(
                f"{KLANTEN_ROOT}klanten?subjectNatuurlijkPersoon__inpBsn=900222086",
                json=paginated_response([self.klant]),
            ),
        ]

    def test_form_is_shown_if_open_klant_configured(self, m):
        self._setUpMocks(m)

        self.assertTrue(self.ok_config.has_api_configuration())

        response = self.app.get(self.case_detail_url, user=self.user)
        contact_form = response.pyquery("#contact-form")

        self.assertTrue(response.context["case"]["contact_moments_enabled"])
        self.assertTrue(contact_form)

    def test_no_form_shown_if_open_klant_not_configured(self, m):
        self._setUpMocks(m)

        # reset
        self.ok_config.klanten_service = None
        self.ok_config.contactmomenten_service = None
        self.ok_config.register_email = ""
        self.ok_config.register_contact_moment = False
        self.ok_config.register_bronorganisatie_rsin = ""
        self.ok_config.register_type = ""
        self.ok_config.register_employee_id = ""
        self.ok_config.save()
        self.assertFalse(self.ok_config.has_api_configuration())

        response = self.app.get(self.case_detail_url, user=self.user)
        contact_form = response.pyquery("#contact-form")

        self.assertFalse(response.context["case"]["contact_moments_enabled"])
        self.assertFalse(contact_form)