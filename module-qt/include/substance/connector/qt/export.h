/*
Copyright 2019 Adobe. All rights reserved.
This file is licensed to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy
of the License at http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS
OF ANY KIND, either express or implied. See the License for the specific language
governing permissions and limitations under the License.
*/

//! @file export.h
//! @brief QObject implementation of the export interface
//! @author Galen Helfter - Adobe
//! @date 20190607
//! @copyright Adobe. All rights reserved.

#pragma once

#include <substance/connector/qt/application.h>

namespace Substance
{
namespace Connector
{
namespace Qt
{
class ConnectorExport : public ConnectorApplication
{
	Q_OBJECT

public:
	ConnectorExport(QObject* parent = nullptr);

	virtual ~ConnectorExport();

	//! @brief Set up the internal state for this implementation
	void initialize() override;

	//! @brief Tear down the internal state
	void shutdown() override;

	//! @brief Send to another application a message to load the sbsar
	//! @param context Integer representing the underlying connection
	//! @param message File path of the sbsar for the other application to load
	void sendLoadSbsar(unsigned int context, const QString& message);

	//! @brief Send to another application a message to load the sbsar
	//! @param context Integer representing the underlying connection
	//! @param message File path of the sbsar for the other application to load
	void sendLoadAsset(unsigned int context, const QString& message);

Q_SIGNALS:
	//! @brief Signal that is emitted when a load sbsar message is received
	//! @param context Integer representing the underlying connection
	//! @param message String value of the received message
	void recvLoadSbsar(unsigned int context, const QString& message);

	//! @brief Signal that is emitted when a load asset message is received
	//! @param context Integer representing the underlying connection
	//! @param message String value of the received message
	void recvLoadAsset(unsigned int context, const QString& message);

	//! @brief Signal that is emitted when an update sbsar message is received
	//! @param context Integer representing the underlying connection
	//! @param message String value of the received message
	void recvUpdateSbsar(unsigned int context, const QString& message);
};
} // namespace Qt
} // namespace Connector
} // namespace Substance
