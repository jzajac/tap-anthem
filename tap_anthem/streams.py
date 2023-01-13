"""Stream type classes for tap-anthem."""

from typing import Iterable

import requests
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_anthem.client import AnthemStream, FormularyNavigatorStream


class NhProvidersStream(AnthemStream):
    """Define custom stream."""
    name = "nh_providers"
    path = "/PROVIDERS_NH.json"
    primary_keys = ["npi"]
    replication_key = "last_updated_on"

    schema = th.PropertiesList(
        th.Property("npi", th.StringType),

        # Applicable where type = 'INDIVIDUAL'
        th.Property("name", th.ObjectType(
            th.Property("first", th.StringType),
            th.Property("middle", th.StringType),
            th.Property("last", th.StringType)
        )),

        # Applicable where type = 'GROUP'
        th.Property("group_name", th.StringType),

        # Applicable where type = 'FACILITY'
        th.Property("facility_name", th.StringType),
        th.Property("facility_type", th.ArrayType(th.StringType)),

        th.Property("type", th.StringType),
        th.Property("accepting", th.StringType),
        th.Property("gender", th.StringType),
        th.Property("languages", th.ArrayType(th.StringType)),
        th.Property("specialty", th.ArrayType(th.StringType)),
        th.Property("addresses", th.ArrayType(
            th.ObjectType(
                th.Property("address", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),  # String to preserve leading zeroes
                th.Property("phone", th.StringType)
            )
        )),
        th.Property("last_updated_on", th.DateTimeType),
        th.Property("plans", th.ArrayType(
            th.ObjectType(
                th.Property("plan_id_type", th.StringType),
                th.Property("plan_id", th.StringType),
                th.Property("network_tier", th.StringType),
                th.Property("years", th.ArrayType(th.IntegerType)),
            )
        ))

    ).to_dict()


class NhPlansStream(AnthemStream):
    """Define custom stream."""
    name = "nh_plans"
    path = '/PLANS_NH.json'
    primary_keys = ["plan_id"]
    replication_key = "last_updated_on"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:

        for row in response.json():
            for formulary in row["formulary"]:
                for costsharing in formulary["costSharing"]:
                    costsharing["pharmacy_type"] = costsharing["pharmacyType"]
                    del costsharing["pharmacyType"]

                    costsharing["copay_amount"] = costsharing["copayAmount"]
                    del costsharing["copayAmount"]

                    costsharing["copay_opt"] = costsharing["copayOpt"]
                    del costsharing["copayOpt"]

                    costsharing["coinsurance_rate"] = costsharing["coinsuranceRate"]
                    del costsharing["coinsuranceRate"]

                    costsharing["coinsurance_opt"] = costsharing["coinsuranceOpt"]
                    del costsharing["coinsuranceOpt"]
                formulary["cost_sharing"] = formulary["costSharing"]
                del formulary["costSharing"]
            yield row

    schema = th.PropertiesList(
        th.Property("plan_id", th.StringType),
        th.Property("plan_id_type", th.StringType),
        th.Property("marketing_name", th.StringType),
        th.Property("summary_url", th.URIType),
        th.Property("plan_contact", th.StringType),
        th.Property("network", th.ArrayType(
            th.ObjectType(
                th.Property("network_tier", th.StringType))
            )
        ),

        th.Property("formulary", th.ArrayType(
            th.ObjectType(
                th.Property("drug_tier", th.StringType),
                th.Property("mail_order", th.BooleanType),
                th.Property("cost_sharing", th.ArrayType(
                    th.ObjectType(
                        th.Property("pharmacy_type", th.StringType),
                        th.Property("copay_amount", th.NumberType),
                        th.Property("copay_opt", th.StringType),
                        th.Property("coinsurance_rate", th.NumberType),
                        th.Property("coinsurance_opt", th.StringType)

                    )
                ))
            )
        )),

        th.Property("years", th.ArrayType(th.IntegerType)),
        th.Property("last_updated_on", th.DateTimeType)
    ).to_dict()


class NhDrugsStream(FormularyNavigatorStream):
    """Define custom stream."""
    name = "drugs_nh"
    path = "/37/drugs.json"
    primary_keys = ["rxnorm_id"]
    # Replication key intentionally omitted
    # No property in source data would be usable for this purpose

    schema = th.PropertiesList(
        th.Property("rxnorm_id", th.StringType),
        th.Property("drug_name", th.StringType),

        th.Property("plans", th.ArrayType(
            th.ObjectType(
                th.Property("plan_id_type", th.StringType),
                th.Property("plan_id", th.StringType),
                th.Property("drug_tier", th.StringType),
                th.Property("prior_authorization", th.BooleanType),
                th.Property("step_therapy", th.BooleanType),
                th.Property("quantity_limit", th.BooleanType),
                th.Property("years", th.ArrayType(th.IntegerType))
            )
        ))
    ).to_dict()