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

import re
import os
import asyncio
import carb
import omni.ext
import omni.ui as ui
from omni.kit.menu.utils import MenuHelperExtension
from omni.kit.viewport.utility import get_active_viewport, frame_viewport_selection
from pxr import Usd, UsdGeom, UsdShade, UsdUtils, Ar, Sdf


# Functions and vars are available to other extensions as usual in python:
# `my_company.my_usd_paths.some_public_function(x)`


def some_public_function(x: int):
    """This is a public function that can be called from other extensions."""
    print(
        f"[my_company.my_usd_paths] some_public_function was called with {x}")

    return x**x


# Any class derived from `omni.ext.IExt` in the top level module (defined in
# `python.modules` of `extension.toml`) will be instantiated when the extension
# gets enabled, and `on_startup(ext_id)` will be called. Later when the
# extension gets disabled on_shutdown() is called.
class MyUSDpaths(omni.ext.IExt, MenuHelperExtension):

    WINDOW_NAME = "My USD Paths"
    MENU_GROUP = "Window"

    def on_startup(self, _ext_id):
        """This is called every time the extension is activated."""
        self._use_regex = False
        self._regex_button = None
        self._regex_button_style = {
            "Button.Label": {"font_size": 12.0},
            "Button": {"margin": 2, "padding": 2},
            "Button:checked": {"background_color": 0xFF114411},
            "Button:hovered": {"background_color": 0xFF444444},
            "Button:pressed": {"background_color": 0xFF111111},
        }
        self._action_button_style = {
            "Button.Label:disabled": {"color": 0xFF666666},
            "Button:disabled": {"background_color": 0xFF222222}
        }

        global _extension_instance
        _extension_instance = self

        global _extension_path
        _extension_path = omni.kit.app.get_app_interface(
        ).get_extension_manager().get_extension_path(_ext_id)

        self._unique_paths = {}
        self._window = None

        ui.Workspace.set_show_window_fn(
            MyUSDpaths.WINDOW_NAME,
            self._show_ui
        )
        self.menu_startup(
            MyUSDpaths.WINDOW_NAME,
            MyUSDpaths.WINDOW_NAME,
            MyUSDpaths.MENU_GROUP
        )

        # self._show_ui(True)
        print("[my_company.my_usd_paths] Extension startup")

    def on_shutdown(self):
        """This is called every time the extension is deactivated. It is used
        to clean up the extension state."""
        global _extension_instance
        global _template_list

        ui.Workspace.set_show_window_fn(MyUSDpaths.WINDOW_NAME, None)
        self.menu_shutdown()
        _extension_instance = None
        _template_list = None

        print("[my_company.my_usd_paths] Extension shutdown")

    def _clean_up_paths_ui(self):
        if hasattr(self, "_scrollable") and self._scrollable is not None:
            self._window.layout.remove_child(self._scrollable)
            self._scrollable = None

    def _list_all_paths(self, path):
        if path not in self._scrollable_pending:
            self._scrollable_pending.append(path)
        return path

    def _modify_path(self, path):
        if path in self._unique_paths:
            return self._unique_paths[path].model.get_value_as_string()

    def _apply_path_edits(self, btn_widget=None):
        stage = omni.usd.get_context().get_stage()
        if not stage:
            carb.log_error("stage not found")
            return

        (all_layers, all_assets, unresolved_paths) = UsdUtils.ComputeAllDependencies(
            stage.GetRootLayer().identifier)
        if not all_layers:
            all_layers = stage.GetLayerStack()
        for layer in all_layers:
            UsdUtils.ModifyAssetPaths(layer, self._modify_path)
        self._traverse()
        self._btn_apply.enabled = False

    def _replace(self, btn_widget=None):
        if not self._unique_paths:
            self._traverse()

        for path in self._unique_paths:
            mdl_path = self._unique_paths[path].model.get_value_as_string()
            if self._use_regex:
                mdl_path = re.sub(
                    self._txt_search.model.get_value_as_string(),
                    self._txt_replace.model.get_value_as_string(),
                    mdl_path,
                )
            else:
                mdl_path = mdl_path.replace(
                    self._txt_search.model.get_value_as_string(
                    ), self._txt_replace.model.get_value_as_string()
                )

            self._unique_paths[path].model.set_value(mdl_path)
        self._btn_apply.enabled = True
        self._btn_replace.enabled = False

    def _toggle_block(self, is_enabled):
        self._txt_search.enabled = is_enabled
        self._txt_replace.enabled = is_enabled
        self._btn_replace.enabled = is_enabled
        if is_enabled:
            return
        self._btn_apply.enabled = False

    async def _wait_frame_finished(self, finish_fn):
        await omni.kit.app.get_app_interface().next_update_async()
        finish_fn()

    async def _preload_materials_from_stage(self, on_complete_fn):
        shaders = []
        stage = omni.usd.get_context().get_stage()
        if not stage:
            carb.log_error("stage not found")
            return

        for p in stage.Traverse():
            if not p.IsA(UsdShade.Material):
                continue
            carb.log_info(f"Found material: {p.GetPath()}")
            if p.GetMetadata("ignore_material_updates"):
                continue
            material = UsdShade.Material(p)
            shader = material.ComputeSurfaceSource("mdl")[0]
            shaders.append(shader.GetPath().pathString)

        old_paths = omni.usd.get_context().get_selection().get_selected_prim_paths()
        omni.usd.get_context().get_selection().set_selected_prim_paths(shaders, True)

        await omni.kit.app.get_app_interface().next_update_async()
        await omni.kit.app.get_app_interface().next_update_async()

        def reload_old_paths():
            omni.usd.get_context().get_selection().set_selected_prim_paths(old_paths, True)
            on_complete_fn()

        asyncio.ensure_future(
            self._wait_frame_finished(finish_fn=reload_old_paths))

    def _traverse(self, btn_widget=None):
        self._unique_paths = {}
        self._scrollable.clear()
        self._scrollable_pending = []
        self._toggle_block(False)

        def on_preload_complete():
            with self._scrollable:
                with ui.VStack(spacing=2, height=0):
                    self._scrollable_pending.sort()
                    for path in self._scrollable_pending:
                        with ui.HStack():
                            text_box = ui.StringField(
                                skip_draw_when_clipped=True)
                            text_box.model.set_value(path)
                            text_box.read_only = True
                            self._unique_paths[path] = text_box

                            def make_find_prims(p=path):
                                def _on_find_prims():
                                    # 延迟清空和重建 UI，避免在 draw/event 期间操作
                                    async def update_ui():
                                        users = self.find_prims_using_asset(p)

                                        def build_result():
                                            self._scrollable.clear()

                                            with self._scrollable:
                                                with ui.VStack(spacing=2, height=0):
                                                    if not users:
                                                        ui.Label(
                                                            f"No prims found using asset: {p}")
                                                        return
                                                    for prim_path in sorted(users):
                                                        with ui.HStack():
                                                            prim_field = ui.StringField(
                                                                skip_draw_when_clipped=True)
                                                            prim_field.model.set_value(
                                                                str(prim_path))
                                                            prim_field.read_only = True

                                                            def make_jump(pp):
                                                                def _on_jump():
                                                                    ctx = omni.usd.get_context()
                                                                    ctx.get_selection().set_selected_prim_paths(
                                                                        [str(pp)], True)
                                                                    frame_viewport_selection(
                                                                        get_active_viewport())
                                                                return _on_jump

                                                            ui.Button(
                                                                "Jump",
                                                                width=0,
                                                                clicked_fn=make_jump(
                                                                    prim_path)
                                                            )

                                        await omni.kit.app.get_app_interface().next_update_async()
                                        build_result()
                                    asyncio.ensure_future(update_ui())
                                return _on_find_prims

                            ui.Button(
                                "Prims",
                                width=0,
                                clicked_fn=make_find_prims(path)
                            )

                    self._scrollable_pending = None

            if len(self._unique_paths) > 0:
                self._toggle_block(True)

        asyncio.ensure_future(
            self.get_asset_paths(
                on_preload_complete,
                self._list_all_paths
            )
        )

    def _build_ui(self):
        with self._window.frame:
            with ui.VStack(spacing=4):
                with ui.VStack(spacing=2, height=0):
                    ui.Spacer(height=4)
                    with ui.HStack(spacing=10, height=0):
                        ui.Label(
                            "Search",
                            width=60,
                            alignment=ui.Alignment.RIGHT_CENTER
                        )

                        with ui.ZStack(height=0):
                            self._txt_search = ui.StringField(
                                identifier="search_string_field"
                            )
                            with ui.HStack():
                                ui.Spacer(height=0)

                                def toggle_regex(button):
                                    self._use_regex = not self._use_regex
                                    button.checked = self._use_regex

                                def on_mouse_hover(hover_state):
                                    self._txt_search.enabled = not hover_state

                                self._regex_button = ui.Button(
                                    width=0, text="Regex", style=self._regex_button_style)
                                self._regex_button.set_clicked_fn(
                                    lambda b=self._regex_button: toggle_regex(b))
                                self._regex_button.set_mouse_hovered_fn(
                                    on_mouse_hover)

                        ui.Spacer(width=10)

                    ui.Spacer()
                    with ui.HStack(spacing=10, height=0):
                        ui.Label("Replace", width=60,
                                 alignment=ui.Alignment.RIGHT_CENTER)
                        self._txt_replace = ui.StringField(
                            height=0, identifier="replace_string_field")
                        ui.Spacer(width=10)
                    ui.Spacer()
                    with ui.HStack(spacing=10):
                        ui.Spacer(width=56)
                        ui.Button(
                            width=0,
                            style=self._action_button_style,
                            clicked_fn=self._traverse,
                            text=" Reload paths ")
                        ui.Spacer()
                        self._btn_replace = ui.Button(
                            width=0,
                            style=self._action_button_style,
                            clicked_fn=self._replace,
                            text=" Preview ",
                            enabled=False)
                        self._btn_apply = ui.Button(
                            width=0,
                            style=self._action_button_style,
                            clicked_fn=self._apply_path_edits,
                            text=" Apply ",
                            enabled=False
                        )
                        ui.Spacer()
                        ui.Spacer(width=100)

                        def on_text_changed(model):
                            if self._btn_apply.enabled:
                                self._btn_apply.enabled = False
                            if not self._btn_replace.enabled:
                                self._btn_replace.enabled = True

                        self._txt_search.model.add_value_changed_fn(
                            on_text_changed)
                        self._txt_replace.model.add_value_changed_fn(
                            on_text_changed)
                        ui.Spacer(width=14)

                self._scrollable = ui.ScrollingFrame(
                    text="ScrollingFrame", vertical_scrollbar_policy=omni.ui.ScrollBarPolicy.SCROLLBAR_ALWAYS_ON
                )

    def _show_ui(self, value):
        if self._window is None:
            self._window = ui.Window(
                self.WINDOW_NAME,
                # width=400,
                # height=200,
                # flags=ui.WINDOW_FLAGS_NO_SCROLLBAR,
                # dockPreference=omni.ui.DockPreference.LEFT_BOTTOM,
            )
            self._window.set_visibility_changed_fn(self._on_visibility_changed)
            self._window.deferred_dock_in(
                "Console",
                ui.DockPolicy.CURRENT_WINDOW_IS_ACTIVE
            )
            self._window.dock_order = 99
            self._build_ui()

        if self._window:
            if value:
                self._window.visible = True
            else:
                self._window.visible = False

    def _on_visibility_changed(self, visible):
        self.menu_refresh()

    async def get_asset_paths(self, on_complete_fn, get_path_fn):
        stage = omni.usd.get_context().get_stage()
        if not stage:
            carb.log_error("stage not found")
            return

        def on_preload_complete():
            (all_layers, all_assets, unresolved_paths) = UsdUtils.ComputeAllDependencies(
                stage.GetRootLayer().identifier
            )
            if not all_layers:
                all_layers = stage.GetLayerStack()
            # all_layers doesn't include session layer, use that too
            session_layer = stage.GetSessionLayer()
            if not session_layer in all_layers:
                all_layers.append(session_layer)

            for layer in all_layers:
                carb.log_warn(
                    f"Modifying asset paths in layer: {layer.identifier}")
                UsdUtils.ModifyAssetPaths(layer, get_path_fn)
            on_complete_fn()

        await self._preload_materials_from_stage(on_preload_complete)

    def find_prims_using_asset(self, asset_path):
        stage = omni.usd.get_context().get_stage()
        users = []
        carb.log_warn(f"Finding prims using asset: {asset_path}")
        for prim in stage.Traverse():
            carb.log_warn(f"  Checking prim: {prim.GetPath()}")
            for attr in prim.GetAttributes():
                name = attr.GetName()
                val = attr.Get()
                if isinstance(val, Sdf.AssetPath):
                    val = val.path
                # carb.log_warn(
                #     f"      Attribute [ {name} ]: {val}")
                if val == asset_path:
                    carb.log_warn(
                        f"      Found asset path in attribute [ {name} ] of prim: {prim.GetPath()}")
                    users.append(prim.GetPath())

            stack = prim.GetPrimStack()
            # carb.log_warn(f"  Checking stack: {stack}")
            for stack_item in stack:
                carb.log_warn(f"    Checking stack: {stack_item}")
                # 合并 payload 和 reference 列表
                payloads = getattr(
                    stack_item.payloadList, "prependedItems", [])
                carb.log_warn(f"      Payloads: {stack_item.payloadList}")
                references = getattr(
                    stack_item.referenceList, "prependedItems", [])
                carb.log_warn(f"      References: {stack_item.referenceList}")
                for item in list(payloads) + list(references):
                    item_asset_path = getattr(item, "assetPath", None)
                    carb.log_warn(f"      AssetPath: {item_asset_path}")
                    if item_asset_path == asset_path:
                        users.append(prim.GetPath())
                        carb.log_warn(
                            f"      Found matching asset path: {item_asset_path}")

            # compQuery = Usd.PrimCompositionQuery(prim)
            # for comp in compQuery.GetCompositionArcs():
            #     target_layer = comp.GetTargetLayer().identifier
            #     carb.log_warn(f"    ArcType: {comp.GetArcType()}")
            #     carb.log_warn(f"    TargetLayer: {target_layer}")
            #     if target_layer == asset_path:
            #         users.append(prim.GetPath(
            #         carb.log_warn(
          #             f"      Found matching target laye)
        return users
