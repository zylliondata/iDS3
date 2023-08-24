# -*- coding: utf-8 -*-
# @Author: 王明浩
# @Date: Created in 15:24 2023/7/21
# @Description: dataset 管理
# @Version: Python 3.8.11
# @Modified By:
import datahub.emitter.mce_builder as builder
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.ingestion.graph.client import DataHubGraph, DatahubClientConfig
from datahub.metadata.com.linkedin.pegasus2avro.dataset import FineGrainedLineage, FineGrainedLineageUpstreamType, \
    FineGrainedLineageDownstreamType, Upstream, DatasetLineageType, UpstreamLineage

from src.config import ioDS3_config


class EntityManagement:

    def __init__(self, server, token):
        self.server = server
        self.token = token

    @classmethod
    def create_client(cls, server, token):
        graph = DataHubGraph(
            config=DatahubClientConfig(
                server=server,
                token=token
            )
        )
        return graph

    def get_list_entities(self, entity_type, start=0, count=10):
        client = self.create_client(self.server, self.token)
        list_entities = client.list_all_entity_urns(entity_type=entity_type, start=start, count=count)
        return list_entities

    def query_entities(self, entity_types, platform=None, env=None, query=None, batch_size=1000):
        client = self.create_client(self.server, self.token)
        results = client.get_urns_by_filter(entity_types=entity_types, platform=platform, env=env, query=query,
                                            batch_size=batch_size)
        lists = []
        for result in results:
            lists.append(result)
        return lists

    def detail_dataset(self, dataset_urn):
        client = self.create_client(self.server, self.token)
        schema = client.get_schema_metadata(entity_urn=dataset_urn)
        schema_items = schema.items()
        result_lists = []
        for item in schema_items:
            # print(item[0], item[1])
            if item[0] == "fields":
                for i in item[1]:
                    dict_item = {'fieldPath': i.fieldPath, 'nativeDataType': i.nativeDataType,
                                 'description': i.description, 'lastModified': i.lastModified}
                    # print(dict_item)
                    result_lists.append(dict_item)
        return result_lists

    def soft_delete_dataset(self, urn):
        client = self.create_client(self.server, self.token)
        flag = client.exists(entity_urn=urn)
        if flag is True:
            client.soft_delete_entity(urn=urn)
            return True
        else:
            return False

    def browse_ui(self, urn):
        return ioDS3_config.get("datahub").get('ui') + "/dataset/" + urn.replace("/", "%2F")

    def create_lineage(self, up_urn, down_urn):
        # client = self.create_client(self.server, self.token)

        lineage_mce = builder.make_lineage_mce(
            [
                up_urn,  # Upstream
            ],
            down_urn,  # Downstream
        )
        emitter = DatahubRestEmitter(gms_server=self.server, token=self.token)
        emitter.emit_mce(lineage_mce)
        emitter.flush()

    def query_lineage(self, urn):
        client = self.create_client(self.server, self.token)
        down_relate = client.get_related_entities(entity_urn=urn,
                                                  relationship_types=['DownstreamOf', 'Schema'],
                                                  direction=client.RelationshipDirection.OUTGOING)
        up_relate = client.get_related_entities(entity_urn=urn,
                                                relationship_types=['UpstreamOf', 'Schema'],
                                                direction=client.RelationshipDirection.INCOMING)
        return up_relate, down_relate

    def create_field_urn(self, dataset_urn, field_path):
        return builder.make_schema_field_urn(parent_urn=dataset_urn, field_path=field_path)

    def create_lineage_streams(self, entities):
        dataset_urn = entities.get('dataset_urn')
        field_path = entities.get('field_path')
        lineage_streams = []
        for field in field_path:
            field_urn = self.create_field_urn(dataset_urn, field)
            lineage_streams.append(field_urn)
        return lineage_streams

    def create_column_lineage(self, up_entities, down_entities):
        # up_entities = {
        #     "dataset_urn": "",
        #     "field_path": []
        # }

        fineGrainedLineages = [
            FineGrainedLineage(
                upstreamType=FineGrainedLineageUpstreamType.FIELD_SET,
                upstreams=self.create_lineage_streams(up_entities),
                downstreamType=FineGrainedLineageDownstreamType.FIELD,
                downstreams=self.create_lineage_streams(down_entities),
            ),
        ]
        upstream = Upstream(
            dataset=up_entities.get('dataset_urn'), type=DatasetLineageType.TRANSFORMED
        )

        fieldLineages = UpstreamLineage(
            upstreams=[upstream], fineGrainedLineages=fineGrainedLineages
        )

        lineage_mcp_column = MetadataChangeProposalWrapper(
            entityUrn=down_entities.get('dataset_urn'),
            aspect=fieldLineages,
        )
        emitter = DatahubRestEmitter(gms_server=self.server, token=self.token)
        emitter.emit_mce(lineage_mcp_column)
        emitter.flush()
