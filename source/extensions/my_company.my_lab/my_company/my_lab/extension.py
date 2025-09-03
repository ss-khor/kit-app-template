# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES.
# All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import omni.ext
import omni.kit.commands
import omni.usd
import omni.ui as ui
import carb
from omni.kit.menu.utils import MenuHelperExtension
from pxr import Usd, Sdf


def create_payload(usd_context: omni.usd.UsdContext, path_to: Sdf.Path, asset_path: str, prim_path: Sdf.Path) -> Usd.Prim:
    omni.kit.commands.execute("CreatePayload",
                              usd_context=usd_context,
                              path_to=path_to,  # Prim path for where to create the prim with the payload
                              # The file path to the payload USD. Relative paths are accepted too.
                              asset_path=asset_path,
                              # OPTIONAL: Prim path to a prim in the payloaded USD, if not provided the default prim is used
                              prim_path=prim_path
                              )
    return usd_context.get_stage().GetPrimAtPath(path_to)


def create_reference(usd_context: omni.usd.UsdContext, path_to: Sdf.Path, asset_path: str, prim_path: Sdf.Path) -> Usd.Prim:
    omni.kit.commands.execute("CreateReference",
                              usd_context=usd_context,
                              path_to=path_to,  # Prim path for where to create the prim with the reference
                              # The file path to reference. Relative paths are accepted too.
                              asset_path=asset_path,
                              # OPTIONAL: Prim path to a prim in the referenced USD, if not provided the default prim is used
                              prim_path=prim_path
                              )
    return usd_context.get_stage().GetPrimAtPath(path_to)

# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.


class MyLab(omni.ext.IExt, MenuHelperExtension):

    WINDOW_NAME = "My Lab"
    MENU_GROUP = "Window"

    def on_startup(self, _ext_id):
        self._window = None

        ui.Workspace.set_show_window_fn(
            MyLab.WINDOW_NAME,
            self._show_ui
        )
        self.menu_startup(
            MyLab.WINDOW_NAME,
            MyLab.WINDOW_NAME,
            MyLab.MENU_GROUP
        )
        # self._show_ui(True)
        print("[my_company.my_lab] Extension startup")

    def on_shutdown(self):
        """This is called every time the extension is deactivated. It is used
        to clean up the extension state."""
        ui.Workspace.set_show_window_fn(MyLab.WINDOW_NAME, None)
        self.menu_shutdown()
        self._window = None
        print("[my_company.my_lab] Extension shutdown")

    def _show_ui(self, value):
        if self._window is None:
            self._window = ui.Window(
                self.WINDOW_NAME,
            )
            self._window.set_visibility_changed_fn(self._on_visibility_changed)
            self._window.deferred_dock_in(
                "Console",
                ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE
            )
            self._window.dock_order = 99
            self._build_ui()
        if self._window:
            self._window.visible = bool(value)

    def _on_visibility_changed(self, visible):
        self.menu_refresh()

    def _build_ui(self):
        with self._window.frame:
            with ui.VStack(spacing=10):
                ui.Label("My Lab Extension", height=0)
                ui.Button("Create Reference", width=0,
                          clicked_fn=self._on_create_reference_clicked)
                ui.Button("Create Payload", width=0,
                          clicked_fn=self._on_create_payload_clicked)

    def _on_create_reference_clicked(self):
        asset_path = "C:/Users/khor.hong.yi/_MySpace_/_SmartScape_/omni/usd/asset_test.usd"
        path_to = Sdf.Path("/World/ref_prim")
        prim_path = Sdf.Path("/World/")

        context: omni.usd.UsdContext = omni.usd.get_context()
        ref_prim: Usd.Prim = create_reference(
            context,
            path_to,
            asset_path,
            prim_path
        )
        # stage: Usd.Stage = context.get_stage()
        # usda = stage.GetRootLayer().ExportToString()
        # carb.log_warn(usda)
        # assert ref_prim.IsValid()
        # assert ref_prim.GetPrimStack()[0].referenceList.prependedItems[0] == Sdf.Reference(
        #     assetPath=asset_path+"/asse", primPath=prim_path)
        carb.log_info("Create Reference button clicked")

    def _on_create_payload_clicked(self):
        asset_path = "C:/Users/khor.hong.yi/_MySpace_/_SmartScape_/omni/usd/asset_test.usd"
        asset_path = "omniverse://192.168.1.30/Library/usd/test.usd"
        path_to = Sdf.Path("/World/payload_prim")
        prim_path = Sdf.Path("/World/")

        context: omni.usd.UsdContext = omni.usd.get_context()
        payload_prim: Usd.Prim = create_payload(
            context,
            path_to,
            asset_path,
            prim_path
        )
        # stage: Usd.Stage = context.get_stage()
        # usda = stage.GetRootLayer().ExportToString()
        # carb.log_warn(usda)
        # assert payload_prim.IsValid()
        # assert payload_prim.GetPrimStack()[0].payloadList.prependedItems[0] == Sdf.Payload(
        #     assetPath=asset_path, primPath=prim_path
        # )
        carb.log_info("Create Payload button clicked")
